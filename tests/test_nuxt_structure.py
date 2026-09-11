from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    target = ROOT / path
    return target.read_text(encoding="utf-8") if target.exists() else ""


class NuxtStructureTests(unittest.TestCase):
    def test_project_declares_nuxt_and_nuxt_ui(self):
        package_path = ROOT / "package.json"
        self.assertTrue(package_path.is_file(), "package.json must define the Nuxt project")
        package = json.loads(package_path.read_text(encoding="utf-8"))
        dependencies = package.get("dependencies", {})
        self.assertIn("nuxt", dependencies)
        self.assertIn("@nuxt/ui", dependencies)
        self.assertEqual(package.get("scripts", {}).get("generate"), "nuxt generate")
        self.assertEqual(package.get("scripts", {}).get("typecheck"), "nuxt typecheck")

    def test_nuxt_config_enables_ui_and_static_prerendering(self):
        config = read("nuxt.config.ts")
        self.assertIn("'@nuxt/ui'", config)
        self.assertRegex(config, r"ssr\s*:\s*true")
        self.assertIn("prerender", config)
        self.assertIn("'/':", config)

    def test_typescript_config_extends_generated_nuxt_config(self):
        config = read("tsconfig.json")
        self.assertIn('"extends": "./.nuxt/tsconfig.json"', config)

    def test_app_uses_nuxt_ui_components_not_only_the_dependency(self):
        app = read("app.vue")
        for component in ("UApp", "UButton", "UBadge", "UCard"):
            with self.subTest(component=component):
                self.assertRegex(app, rf"<{component}(?:\s|>)")

    def test_public_files_are_in_nuxt_public_directory(self):
        self.assertEqual(read("public/CNAME").strip(), "bpy.dev")
        image = ROOT / "public/assets/blenderbench-result.webp"
        self.assertTrue(image.is_file(), "benchmark image must be served from public/assets")

    def test_pages_workflow_builds_and_uploads_generated_output(self):
        workflow = read(".github/workflows/pages.yml")
        for expected in (
            "pnpm/action-setup@",
            "actions/setup-node@",
            "pnpm install --frozen-lockfile",
            "pnpm test",
            "pnpm typecheck",
            "pnpm generate",
            "path: .output/public",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, workflow)
        self.assertNotRegex(workflow, r"uses:\s+[^\s]+@v\d+")

    def test_superseded_root_static_entrypoints_are_removed(self):
        for path in ("index.html", "styles.css", "script.js", "CNAME"):
            with self.subTest(path=path):
                self.assertFalse((ROOT / path).exists(), f"{path} is superseded by Nuxt")

    def test_generated_and_dependency_directories_are_ignored(self):
        for path in ("node_modules/example", ".nuxt/example", ".output/example", "dist"):
            with self.subTest(path=path):
                result = subprocess.run(
                    ["git", "check-ignore", "--quiet", "--no-index", path], cwd=ROOT, check=False
                )
                self.assertEqual(result.returncode, 0, f"{path} must be ignored")


if __name__ == "__main__":
    unittest.main(verbosity=2)
