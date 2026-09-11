from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / ".output" / "public"
INDEX = OUTPUT / "index.html"
IMAGE = OUTPUT / "assets" / "blenderbench-result.webp"


def read_site_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def relative_luminance(hex_color: str) -> float:
    channels = [int(hex_color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return sum(weight * channel for weight, channel in zip((0.2126, 0.7152, 0.0722), linear))


def contrast_ratio(first: str, second: str) -> float:
    lighter, darker = sorted(
        (relative_luminance(first), relative_luminance(second)), reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)


class Document(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.direct_children: dict[int, list[str]] = {}
        self.open_tags: list[tuple[str, int]] = []
        self.text_parts: list[str] = []
        self.ignored_depth = 0

    def handle_starttag(self, tag: str, attrs):
        self.tags.append((tag, dict(attrs)))
        index = len(self.tags) - 1
        if self.open_tags:
            self.direct_children.setdefault(self.open_tags[-1][1], []).append(tag)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.open_tags.append((tag, index))
        if tag in {"script", "style"}:
            self.ignored_depth += 1

    def handle_endtag(self, tag: str):
        if tag in {"script", "style"}:
            self.ignored_depth -= 1
        for offset in range(len(self.open_tags) - 1, -1, -1):
            if self.open_tags[offset][0] == tag:
                del self.open_tags[offset:]
                break

    def handle_data(self, data: str):
        if not self.ignored_depth:
            self.text_parts.append(data)

    @property
    def text(self) -> str:
        text = " ".join(" ".join(self.text_parts).split())
        return re.sub(r"\s+([.,;:])", r"\1", text)

    def attrs_for(self, tag: str) -> list[dict[str, str | None]]:
        return [attrs for found, attrs in self.tags if found == tag]


class StaticHomepageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = read_site_file(INDEX)
        cls.css = "\n".join(read_site_file(path) for path in sorted((OUTPUT / "_nuxt").glob("*.css")))
        cls.js = "\n".join(read_site_file(path) for path in sorted((OUTPUT / "_nuxt").glob("*.js")))
        cls.source = read_site_file(ROOT / "app.vue")
        cls.source_css = read_site_file(ROOT / "assets/css/main.css")
        cls.doc = Document(cls.html)
        cls.doc.feed(cls.html)
        cls.text = cls.doc.text

    def test_primary_message_leads_with_image_to_headless_blender_workflow(self):
        h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", self.html, flags=re.I | re.S)
        self.assertEqual(len(h1), 1)
        heading = re.sub(r"<[^>]+>", " ", h1[0])
        heading = " ".join(heading.split()).lower()
        self.assertIn("give your agent a reference image", heading)
        self.assertIn("build the blender scene", heading)
        self.assertLess(self.text.lower().find("give your agent a reference image"), 1_000)

    def test_video_explains_the_reference_to_cli_workflow_before_playback(self):
        intro = re.search(
            r'<div class="hero-demo-intro">(?P<body>.*?)</div>',
            self.html,
            flags=re.S,
        )
        self.assertIsNotNone(intro)
        assert intro
        self.assertLess(intro.end(), self.html.index("<video", intro.end()))
        intro_text = " ".join(re.sub(r"<[^>]+>", " ", intro.group("body")).split())
        for phrase in (
            "Reference image → agent → headless Blender",
            "without opening the GUI",
            "writes Python through the CLI",
            "renders headlessly",
            "inspects the result",
            "iterates",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, intro_text)

    def test_page_heading_precedes_demo_styling_text_semantically(self):
        headings = re.findall(r"<h([1-6])\b", self.html, flags=re.I)
        self.assertTrue(headings)
        self.assertEqual(headings[0], "1")
        intro = re.search(
            r'<div class="hero-demo-intro">(?P<body>.*?)</div>',
            self.html,
            flags=re.S,
        )
        self.assertIsNotNone(intro)
        assert intro
        self.assertNotRegex(intro.group("body"), r"<h[1-6]\b")

    def test_community_preview_and_verified_evidence_are_present(self):
        required = [
            "Open community preview",
            "27 public BlenderBench tasks",
            "10 rounds per task",
            "270 GPU-rendered and GPU-CLIP-scored checkpoints",
            "exactly four MCP tools",
            "no VLM judge",
            "no score feedback during generation",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.text.lower())

    def test_category_n_clip_results_and_definition_are_precise(self):
        for category, value in [
            ("Camera / Level 1", "0.3738476170433892"),
            ("Level 2", "1.603147718641493"),
            ("Level 3", "2.2820386621687145"),
        ]:
            with self.subTest(category=category):
                self.assertIn(category, self.text)
                self.assertIn(value, self.text)
        self.assertIn("category mean best n-clip ×100", self.text.lower())
        self.assertIn("lower is better", self.text.lower())
        self.assertIn("CLIP image-embedding cosine similarity", self.text)
        self.assertEqual(self.text.count("CLIP accuracy"), 1)

    def test_benchmark_caveats_are_explicit(self):
        for caveat in [
            "public dataset",
            "no official hidden evaluation or leaderboard",
            "not a controlled same-model, same-budget VIGA comparison",
        ]:
            with self.subTest(caveat=caveat):
                self.assertIn(caveat.lower(), self.text.lower())
        self.assertIn(
            "the image itself says “clip accuracy,” but this is cosine similarity, not literal accuracy",
            self.text.lower(),
        )

    def test_benchmark_visual_has_dataset_and_license_attribution(self):
        self.assertIn("BlenderBench by DietCoke4671 and contributors", self.text)
        self.assertIn("203e4d325e9438ca55b29bdfc4f6a90842d74e68", self.text)
        self.assertIn("CC BY 4.0", self.text)
        hrefs = {attrs.get("href") for attrs in self.doc.attrs_for("a")}
        self.assertIn("https://huggingface.co/datasets/DietCoke4671/BlenderBench", hrefs)
        self.assertIn("https://creativecommons.org/licenses/by/4.0/", hrefs)

    def test_how_it_works_follows_reference_build_inspect_sequence(self):
        sequence = "Reference → Build → Inspect"
        start = self.text.find(sequence)
        positions = [self.text.find(label, start) for label in ["Reference", "Build", "Inspect"]]
        self.assertTrue(all(position >= 0 for position in positions))
        self.assertEqual(positions, sorted(positions))
        self.assertIn(sequence, self.text)
        self.assertIn("The agent gets an image and a goal", self.text)
        self.assertIn("runs Blender as a headless backend", self.text)
        self.assertIn("renders its own work, looks at the result, and keeps going", self.text)

    def test_public_links_are_exact_and_build_work_is_not_overclaimed(self):
        hrefs = {attrs.get("href") for attrs in self.doc.attrs_for("a")}
        for href in [
            "https://github.com/bpy-dev/blender-mcp",
            "https://github.com/bpy-dev/blender-mcp/issues",
            "https://github.com/michaelgold/buildbpy/pull/9",
        ]:
            self.assertIn(href, hrefs)
        self.assertIn("work in progress", self.text.lower())
        prohibited = [
            r"buildbpy.{0,50}\b(?:merged|released|published)\b",
            r"\b(?:released|published) enhanced bpy\b",
            r"\bstate[- ]of[- ]the[- ]art\b",
            r"\bSOTA\b",
            r"\bbeats? VIGA\b",
            r"\bproduction[- ]ready\b",
        ]
        for pattern in prohibited:
            with self.subTest(pattern=pattern):
                self.assertIsNone(re.search(pattern, self.text, flags=re.I))

    def test_footer_has_independent_project_and_trademark_disclaimer(self):
        self.assertIn(
            "bpy.dev is an independent community project and not an official Blender Foundation product",
            self.text,
        )
        self.assertIn(
            "“Blender” and the Blender logo are Blender Foundation trademarks",
            self.text,
        )

    def test_semantic_structure_navigation_and_ctas_are_accessible(self):
        tags = [tag for tag, _ in self.doc.tags]
        for tag in ["header", "nav", "main", "section", "footer"]:
            self.assertIn(tag, tags)
        self.assertEqual(len(self.doc.attrs_for("h1")), 1)
        self.assertTrue(any(a.get("href") == "#main-content" and "skip" in (a.get("class") or "") for a in self.doc.attrs_for("a")))
        self.assertTrue(any(a.get("aria-label") for a in self.doc.attrs_for("nav")))
        self.assertTrue(any("button" in (a.get("class") or "") for a in self.doc.attrs_for("a")))
        images = self.doc.attrs_for("img")
        self.assertTrue(images)
        self.assertTrue(all((i.get("alt") or "").strip() for i in images))

    def test_aria_labels_use_semantic_elements_or_explicit_roles(self):
        labelled_divs = [
            attrs
            for tag, attrs in self.doc.tags
            if tag == "div" and attrs.get("aria-label")
        ]
        for attrs in labelled_divs:
            with self.subTest(class_name=attrs.get("class")):
                self.assertIn(attrs.get("role"), {"group", "region"})

        actions = next(attrs for tag, attrs in self.doc.tags if "actions" in (attrs.get("class") or "").split())
        hero_video = next(
            (tag, attrs)
            for tag, attrs in self.doc.tags
            if "hero-video-card" in (attrs.get("class") or "").split()
        )
        footer_links = next((tag, attrs) for tag, attrs in self.doc.tags if "footer-links" in (attrs.get("class") or "").split())
        self.assertEqual(actions.get("role"), "group")
        self.assertEqual(hero_video[0], "figure")
        self.assertEqual(footer_links[0], "nav")

        results_region = next(
            attrs
            for tag, attrs in self.doc.tags
            if tag == "div" and "results-table-wrap" in (attrs.get("class") or "").split()
        )
        self.assertEqual(results_region.get("role"), "region")
        self.assertEqual(results_region.get("aria-label"), "Category mean best N-CLIP times 100")

    def test_video_figcaption_is_a_direct_child_of_its_figure(self):
        figure_index = next(
            index
            for index, (tag, attrs) in enumerate(self.doc.tags)
            if tag == "figure" and "hero-video-card" in (attrs.get("class") or "").split()
        )
        children = self.doc.direct_children.get(figure_index, [])
        self.assertIn("video", children)
        self.assertEqual(children[-1], "figcaption")

    def test_generated_resource_hints_and_tables_are_valid_html(self):
        for attrs in self.doc.attrs_for("link"):
            if attrs.get("as"):
                self.assertIn(attrs.get("rel"), {"preload", "modulepreload"})

        without_comments = re.sub(r"<!--.*?-->", "", self.html, flags=re.DOTALL)
        self.assertNotRegex(without_comments, r"<tr\b[^>]*>\s*</tr>")

    def test_nuxt_ui_badge_preserves_compact_accessible_eyebrow(self):
        eyebrow = re.search(r"\.eyebrow\s*\{([^}]*)\}", self.source_css)
        self.assertIsNotNone(eyebrow)
        assert eyebrow
        rules = eyebrow.group(1).replace(" ", "").lower()
        self.assertIn("display:inline-flex", rules)
        self.assertIn("width:fit-content", rules)
        self.assertIn("background:transparent", rules)
        self.assertIn("color:#313131", rules)

    def test_normal_text_color_tokens_meet_wcag_aa(self):
        blue = re.search(r"--blue:\s*(#[0-9a-fA-F]{6})", self.css)
        video_caption = re.search(r"\.hero-video-caption\s*\{[^}]*color:\s*(#[0-9a-fA-F]{6})", self.css)
        preview_kicker = re.search(r"\.preview \.kicker\s*\{([^}]*)\}", self.css)
        self.assertIsNotNone(blue)
        self.assertIsNotNone(video_caption)
        self.assertIsNotNone(preview_kicker)
        assert blue and video_caption and preview_kicker

        self.assertEqual(blue.group(1).lower(), "#1464f4")
        self.assertGreaterEqual(contrast_ratio(blue.group(1), "#f7f7f5"), 4.5)
        self.assertGreaterEqual(contrast_ratio(blue.group(1), "#ffffff"), 4.5)
        self.assertEqual(video_caption.group(1).lower(), "#b2b5bd")
        self.assertGreaterEqual(contrast_ratio(video_caption.group(1), "#0d0f13"), 4.5)
        self.assertRegex(preview_kicker.group(1), r"opacity:\s*1(?:\.0+)?(?:;|$)")

    def test_mobile_navigation_has_real_toggle_and_progressive_fallback(self):
        buttons = self.doc.attrs_for("button")
        menu = next((b for b in buttons if b.get("aria-controls") == "site-nav"), None)
        self.assertIsNotNone(menu)
        assert menu is not None
        self.assertEqual(menu.get("aria-expanded"), "false")
        self.assertIn("@media (max-width: 760px)", self.source_css)
        self.assertRegex(self.source_css, r"\.nav-toggle\s*\{[^}]*display:\s*none")
        self.assertIn(".nav-toggle", self.source_css)
        self.assertIn("aria-expanded", self.source)
        self.assertIn("Escape", self.source)

    def test_reduced_motion_and_visible_focus_are_supported(self):
        self.assertIn("@media (prefers-reduced-motion: reduce)", self.source_css)
        self.assertIn(":focus-visible", self.css)

    def test_hero_video_precedes_copy_in_dom_and_visual_order(self):
        self.assertLess(
            self.source.index('<figure class="hero-video-card">'),
            self.source.index('<div class="hero-copy">'),
        )
        self.assertNotRegex(self.source_css, r"\.hero-video-card\{[^}]*order:")

    def test_hero_video_never_autoplays_before_user_action(self):
        video = next(
            attrs
            for attrs in self.doc.attrs_for("video")
            if "hero-video-player" in (attrs.get("class") or "").split()
        )
        self.assertNotIn("autoplay", video)
        self.assertNotRegex(self.source, r"\.play\s*\(")

    def test_hero_video_does_not_download_media_during_initial_load(self):
        video = next(
            attrs
            for attrs in self.doc.attrs_for("video")
            if "hero-video-player" in (attrs.get("class") or "").split()
        )
        self.assertEqual(video.get("preload"), "none")

    def test_hugging_face_video_fallback_is_visible_in_the_caption(self):
        video_url = (
            "https://huggingface.co/datasets/michaelgold/blenderbench-direct-results/resolve/"
            "7c2c43be4517aee4d76d2b445578988de186970c/video/"
            "blenderbench-complete-compilation.mp4"
        )
        caption = re.search(
            r'<figcaption class="hero-video-caption">(?P<body>.*?)</figcaption>',
            self.html,
            flags=re.S,
        )
        self.assertIsNotNone(caption)
        assert caption
        self.assertIn(f'href="{video_url}"', caption.group("body"))
        self.assertIn("Watch/download on Hugging Face", caption.group("body"))

    def test_video_has_a_linked_visible_descriptive_results_alternative(self):
        caption = re.search(
            r'<figcaption class="hero-video-caption">(?P<body>.*?)</figcaption>',
            self.html,
            flags=re.S,
        )
        self.assertIsNotNone(caption)
        assert caption
        self.assertIn('href="#blenderbench-video-description"', caption.group("body"))

        description = re.search(
            r'<div id="blenderbench-video-description"[^>]*>(?P<body>.*?)</div>',
            self.html,
            flags=re.S,
        )
        self.assertIsNotNone(description)
        assert description
        text = " ".join(re.sub(r"<[^>]+>", " ", description.group("body")).split())
        for phrase in (
            "27 tasks and 270 rounds",
            "task and round",
            "generated scene beside its target render",
            "CLIP image-embedding cosine similarity",
            "generated Python token count",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertIn(
            "results/results-summary.json",
            description.group("body"),
        )

    def test_social_search_and_viewport_metadata_are_complete(self):
        metas = self.doc.attrs_for("meta")
        by_name = {m.get("name"): m.get("content") for m in metas if m.get("name")}
        by_property = {m.get("property"): m.get("content") for m in metas if m.get("property")}
        for name in ["description", "viewport", "twitter:card", "twitter:title", "twitter:description", "twitter:image"]:
            self.assertTrue(by_name.get(name), name)
        for prop in ["og:type", "og:url", "og:title", "og:description", "og:image", "og:image:alt"]:
            self.assertTrue(by_property.get(prop), prop)
        self.assertEqual(by_property["og:url"], "https://bpy.dev/")
        self.assertEqual(by_property["og:image"], "https://bpy.dev/assets/blenderbench-result.webp")
        self.assertTrue(any(link.get("rel") == "canonical" and link.get("href") == "https://bpy.dev/" for link in self.doc.attrs_for("link")))

    def test_existing_result_image_integrity_and_reference(self):
        self.assertEqual(hashlib.sha256(IMAGE.read_bytes()).hexdigest(), "39702ee8d982154555b471a55deb4a14127b6a12e5b6958b4efb64cc495f55ca")
        image = next((i for i in self.doc.attrs_for("img") if i.get("src") == "/assets/blenderbench-result.webp"), {})
        self.assertEqual(image.get("width"), "1280")
        self.assertEqual(image.get("height"), "720")

    def test_latest_compilation_video_is_in_hero_and_readme(self):
        video_url = (
            "https://huggingface.co/datasets/michaelgold/blenderbench-direct-results/resolve/"
            "7c2c43be4517aee4d76d2b445578988de186970c/video/"
            "blenderbench-complete-compilation.mp4"
        )
        video = re.search(r"<video(?P<attrs>[^>]*)>", self.source, flags=re.S)
        self.assertIsNotNone(video)
        assert video
        self.assertIn('class="hero-video-player"', video.group("attrs"))
        for attribute in ("muted", "playsinline", "controls"):
            with self.subTest(attribute=attribute):
                self.assertRegex(video.group("attrs"), rf"\b{attribute}\b")
        for attribute in ("autoplay", "loop"):
            with self.subTest(attribute=attribute):
                self.assertNotRegex(video.group("attrs"), rf"\b{attribute}\b")
        self.assertIn('preload="none"', video.group("attrs"))
        self.assertIn('poster="/assets/blenderbench-result.webp"', self.source)
        self.assertIn(video_url, self.source)
        self.assertIn("CLIP image-embedding cosine similarity", self.source)
        self.assertIn(video_url, read_site_file(ROOT / "README.md"))

    def test_pages_configuration_and_readme_are_present(self):
        self.assertEqual(read_site_file(ROOT / "public/CNAME").strip(), "bpy.dev")
        workflow = read_site_file(ROOT / ".github/workflows/pages.yml")
        self.assertIn("actions/upload-pages-artifact", workflow)
        self.assertIn("actions/deploy-pages", workflow)
        self.assertIn("permissions:", workflow)
        self.assertIn("pnpm generate", workflow)
        self.assertIn("path: .output/public", workflow)
        readme = read_site_file(ROOT / "README.md")
        self.assertIn("pnpm dev", readme)
        self.assertIn("pnpm generate", readme)
        self.assertIn("GitHub Pages", readme)
        self.assertIn("bpy.dev", readme)

    def test_all_local_references_resolve(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/check_local_refs.py"), str(OUTPUT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 missing local references", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
