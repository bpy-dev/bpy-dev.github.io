<script setup lang="ts">
const navOpen = ref(false)

const benchmarkRows = [
  { category: 'Camera / Level 1', score: '0.3738476170433892' },
  { category: 'Level 2', score: '1.603147718641493' },
  { category: 'Level 3', score: '2.2820386621687145' }
]


const closeNav = () => {
  navOpen.value = false
}

const onKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && navOpen.value) {
    closeNav()
    document.querySelector<HTMLButtonElement>('.nav-toggle')?.focus()
  }
}

const onResize = () => {
  if (window.matchMedia('(min-width: 761px)').matches) closeNav()
}

onMounted(() => {
  document.addEventListener('keydown', onKeydown)
  window.addEventListener('resize', onResize)
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKeydown)
  window.removeEventListener('resize', onResize)
})

useHead({
  title: 'bpy.dev — Headless Blender for agents',
  link: [{ rel: 'canonical', href: 'https://bpy.dev/' }]
})

useSeoMeta({
  description: 'Give an agent a reference image and let it build in Blender through a narrow CLI and MCP interface—headlessly, without opening the GUI.',
  ogType: 'website',
  ogUrl: 'https://bpy.dev/',
  ogTitle: 'bpy.dev — Headless Blender for agents',
  ogDescription: 'Give an agent a reference image. Let it build, render, inspect, and iterate in Blender through the CLI.',
  ogImage: 'https://bpy.dev/assets/blenderbench-result.webp',
  ogImageAlt: 'A BlenderBench generated bedroom scene shown beside its target render.',
  twitterCard: 'summary_large_image',
  twitterTitle: 'bpy.dev — Headless Blender for agents',
  twitterDescription: 'Give an agent a reference image. Let it build, render, inspect, and iterate in Blender through the CLI.',
  twitterImage: 'https://bpy.dev/assets/blenderbench-result.webp'
})
</script>

<template>
  <UApp>
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header class="site-header">
      <div class="shell header-inner">
        <a class="brand" href="#top" aria-label="bpy.dev home">
          <span class="brand-mark" aria-hidden="true"><i /><i /><i /></span>
          <span>bpy.dev</span>
        </a>
        <button
          class="nav-toggle"
          type="button"
          :aria-expanded="navOpen"
          aria-controls="site-nav"
          @click="navOpen = !navOpen"
        >
          <span class="sr-only">Toggle navigation</span>
          <span class="nav-toggle-lines" aria-hidden="true" />
        </button>
        <nav id="site-nav" class="site-nav" :class="{ 'is-open': navOpen }" aria-label="Primary navigation">
          <a href="#capabilities" @click="closeNav">Capabilities</a>
          <a href="#architecture" @click="closeNav">How it works</a>
          <a href="#evidence" @click="closeNav">Evidence</a>
          <UButton class="button button-small button-dark" color="neutral" href="https://github.com/bpy-dev/blender-mcp">View source <span aria-hidden="true">↗</span></UButton>
        </nav>
      </div>
    </header>

    <main id="main-content">
      <section id="top" class="hero" aria-labelledby="hero-title">
        <div class="hero-grid" aria-hidden="true"><span /><span /><span /></div>
        <div class="shell hero-layout">
          <figure class="hero-video-card">
            <div class="hero-demo-intro">
              <p class="mini-label">Reference image → agent → headless Blender</p>
              <h2>Watch an agent rebuild images without opening the GUI.</h2>
              <p>It reads the reference, writes Python through the CLI, renders headlessly, inspects the result, and iterates.</p>
            </div>
            <div class="hero-video-topbar"><span>BlenderBench / Run 001</span><span>27 tasks · 270 rounds</span></div>
            <video
              class="hero-video-player"
              muted
              playsinline
              controls
              preload="none"
              poster="/assets/blenderbench-result.webp"
              aria-label="BlenderBench run showing generated Blender scenes beside target renders across 27 tasks"
            >
              <source src="https://huggingface.co/datasets/michaelgold/blenderbench-direct-results/resolve/7c2c43be4517aee4d76d2b445578988de186970c/video/blenderbench-complete-compilation.mp4" type="video/mp4">
              <a href="https://huggingface.co/datasets/michaelgold/blenderbench-direct-results/resolve/7c2c43be4517aee4d76d2b445578988de186970c/video/blenderbench-complete-compilation.mp4">Watch the BlenderBench compilation video</a>.
            </video>
            <figcaption class="hero-video-caption">
              <span>The full run: reference image and generated scene, task by task.</span>
              <span>The on-screen percentage is CLIP image-embedding cosine similarity—not literal task accuracy.</span>
              <span class="hero-video-links"><a href="#blenderbench-video-description">Read the video description and results</a> · <a href="https://huggingface.co/datasets/michaelgold/blenderbench-direct-results/resolve/7c2c43be4517aee4d76d2b445578988de186970c/video/blenderbench-complete-compilation.mp4">Watch/download on Hugging Face</a></span>
            </figcaption>
          </figure>
          <div class="hero-copy">
            <UBadge class="eyebrow" color="neutral" variant="subtle"><span class="status-dot" aria-hidden="true" /> Open community preview</UBadge>
            <h1 id="hero-title">Give your agent a reference image. Let it build the Blender scene.</h1>
            <p class="hero-lede"><strong>blender-mcp makes Blender a headless backend for coding agents.</strong> The agent uses the image as its goal, drives Blender through a narrow CLI and MCP surface, then renders and inspects its own work as it goes.</p>
            <div class="actions" role="group" aria-label="Project links">
              <UButton class="button button-primary" href="https://github.com/bpy-dev/blender-mcp">Explore blender-mcp <span aria-hidden="true">↗</span></UButton>
              <UButton class="button button-secondary" color="neutral" variant="outline" href="https://github.com/bpy-dev/blender-mcp/issues">Give feedback <span aria-hidden="true">→</span></UButton>
            </div>
            <p class="hero-note">Standalone bpy packaging remains work in progress. <a href="https://github.com/michaelgold/buildbpy/pull/9">Track build work in PR #9</a>.</p>
          </div>
        </div>
      </section>

      <section id="capabilities" class="capabilities rule-top" aria-labelledby="capabilities-title">
        <div class="shell">
          <div class="section-heading">
            <p class="kicker">01 / What developers can do</p>
            <h2 id="capabilities-title">Blender is the backend. Your agent does the work.</h2>
            <p>Use the same Python runtime directly, or expose a small set of operations to an agent.</p>
          </div>
          <div class="capability-grid">
            <UCard class="capability-card" as="article" :ui="{ body: 'contents' }">
              <span class="card-index" aria-hidden="true">A</span>
              <div><h3>Use it from Python</h3><p>Build render pipelines, tests, and batch jobs around <code>import bpy</code> in a normal Python workflow.</p></div>
              <span class="card-tag">Python API</span>
            </UCard>
            <UCard class="capability-card capability-card-dark" as="article" :ui="{ body: 'contents' }">
              <span class="card-index" aria-hidden="true">B</span>
              <div><h3>Let an agent drive it</h3><p>Give an agent four CLI-friendly MCP tools to write Python, render the scene, inspect the image, and keep working.</p></div>
              <a class="card-link" href="https://github.com/bpy-dev/blender-mcp">Inspect the interface <span aria-hidden="true">↗</span></a>
            </UCard>
          </div>
        </div>
      </section>

      <section id="architecture" class="architecture rule-top" aria-labelledby="architecture-title">
        <div class="shell architecture-layout">
          <div class="section-heading architecture-intro">
            <p class="kicker">02 / How it works</p>
            <h2 id="architecture-title">Reference → Build → Inspect</h2>
            <p>The loop is visual, but the backend is headless. No one has to sit in front of Blender.</p>
          </div>
          <ol class="architecture-flow">
            <li><span class="flow-number">01</span><div><h3>Reference</h3><p>The agent gets an image and a goal—rebuild what it sees as a real Blender scene.</p></div></li>
            <li><span class="flow-number">02</span><div><h3>Build</h3><p>It writes Python through the CLI and runs Blender as a headless backend.</p></div></li>
            <li><span class="flow-number">03</span><div><h3>Inspect</h3><p>It renders its own work, looks at the result, and keeps going. The GUI never needs to open.</p></div></li>
          </ol>
        </div>
      </section>

      <section id="evidence" class="evidence rule-top" aria-labelledby="evidence-title">
        <div class="shell">
          <div class="section-heading evidence-heading">
            <p class="kicker">03 / Initial evidence</p>
            <h2 id="evidence-title">Measured in renders, not claims.</h2>
            <p>One transparent community-preview run on the public BlenderBench dataset.</p>
          </div>
          <dl class="stat-grid" aria-label="Benchmark run totals">
            <div><dt>27</dt><dd>public BlenderBench tasks</dd></div>
            <div><dt>270</dt><dd>GPU-rendered and GPU-CLIP-scored checkpoints</dd></div>
            <div><dt>4</dt><dd>exactly four MCP tools</dd></div>
          </dl>
          <div class="method-strip"><span>10 rounds per task</span><span>no VLM judge</span><span>no score feedback during generation</span></div>

          <div id="blenderbench-video-description" class="video-description">
            <p class="mini-label">Video description and results</p>
            <h3>Text alternative for the silent compilation</h3>
            <p>The compilation covers 27 tasks and 270 rounds. Each checkpoint identifies its task and round, places the generated scene beside its target render, and reports the CLIP image-embedding cosine similarity and generated Python token count shown on screen.</p>
            <p><a href="https://huggingface.co/datasets/michaelgold/blenderbench-direct-results/resolve/7c2c43be4517aee4d76d2b445578988de186970c/results/results-summary.json">Open the detailed per-task results on Hugging Face</a>.</p>
          </div>

          <div class="results-layout">
            <div class="results-copy">
              <p class="mini-label">Category results</p>
              <h3>Mean best distance by difficulty</h3>
              <p><strong>Category mean best N-CLIP ×100</strong>. N-CLIP is derived from CLIP image-embedding cosine similarity; lower is better. Values retain the precision of the recorded aggregate.</p>
            </div>
            <div class="results-table-wrap" role="region" aria-label="Category mean best N-CLIP times 100">
              <span class="sr-only">Category mean best N-CLIP times 100</span>
              <table class="results-table">
                <thead>
                  <tr><th scope="col">Category</th><th scope="col">N-CLIP ×100</th></tr>
                </thead>
                <tbody>
                  <tr v-for="row in benchmarkRows" :key="row.category">
                    <td>{{ row.category }}</td><td>{{ row.score }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <figure class="benchmark-figure">
            <div class="image-frame">
              <img src="/assets/blenderbench-result.webp" width="1280" height="720" loading="lazy" alt="Best-round generated bedroom scene beside the BlenderBench target render for task 24 of 27, round 7 of 10.">
              <span class="image-label" aria-hidden="true">RUN 001 / TASK 024 / ROUND 07</span>
            </div>
            <figcaption>
              <span>Best-round checkpoint and target from the initial run.</span>
              <span class="attribution">Target data: <a href="https://huggingface.co/datasets/DietCoke4671/BlenderBench">BlenderBench by DietCoke4671 and contributors</a>, dataset revision <code>203e4d325e9438ca55b29bdfc4f6a90842d74e68</code>, licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</span>
            </figcaption>
          </figure>

          <aside class="caveat" aria-labelledby="caveat-title">
            <p id="caveat-title" class="mini-label">Read this result correctly</p>
            <p>This is a first run on a <strong>public dataset</strong>. There is <strong>no official hidden evaluation or leaderboard</strong>, and this is <strong>not a controlled same-model, same-budget VIGA comparison</strong>. The image itself says “CLIP accuracy,” but this is cosine similarity, not literal accuracy. Treat it as inspectable initial evidence—not a ranking.</p>
          </aside>
        </div>
      </section>

      <section id="preview" class="preview rule-top" aria-labelledby="preview-title">
        <div class="shell preview-panel">
          <div><p class="kicker">Open community preview</p><h2 id="preview-title">Test the boundary. Question the benchmark. Shape what ships.</h2></div>
          <div class="preview-actions">
            <UButton class="button button-primary" color="neutral" href="https://github.com/bpy-dev/blender-mcp/issues">Open an issue <span aria-hidden="true">↗</span></UButton>
            <a class="text-link" href="https://github.com/michaelgold/buildbpy/pull/9">Follow standalone bpy build work <span aria-hidden="true">↗</span></a>
          </div>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <div class="shell footer-grid">
        <div><a class="brand footer-brand" href="#top">bpy.dev</a><p>Blender, made composable.</p></div>
        <nav class="footer-links" aria-label="Project links">
          <a href="https://github.com/bpy-dev/blender-mcp">blender-mcp</a>
          <a href="https://github.com/bpy-dev/blender-mcp/issues">Issues</a>
          <a href="https://huggingface.co/datasets/DietCoke4671/BlenderBench">BlenderBench dataset</a>
        </nav>
        <p class="footer-note">Community preview. Interfaces and results may change as feedback arrives.</p>
        <p class="footer-legal">bpy.dev is an independent community project and not an official Blender Foundation product. “Blender” and the Blender logo are Blender Foundation trademarks.</p>
      </div>
    </footer>
  </UApp>
</template>
