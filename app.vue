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
  title: 'bpy.dev — Blender for Python and agents',
  link: [{ rel: 'canonical', href: 'https://bpy.dev/' }]
})

useSeoMeta({
  description: 'Use Blender as a Python module and give agents a narrow MCP interface. Explore the open community preview and its first BlenderBench results.',
  ogType: 'website',
  ogUrl: 'https://bpy.dev/',
  ogTitle: 'bpy.dev — Blender for Python and agents',
  ogDescription: 'A Python-first Blender runtime and a narrow, auditable MCP interface for agents.',
  ogImage: 'https://bpy.dev/assets/blenderbench-result.webp',
  ogImageAlt: 'A BlenderBench generated bedroom scene shown beside its target render.',
  twitterCard: 'summary_large_image',
  twitterTitle: 'bpy.dev — Blender for Python and agents',
  twitterDescription: 'A Python-first Blender runtime and a narrow, auditable MCP interface for agents.',
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
          <a href="#architecture" @click="closeNav">Architecture</a>
          <a href="#evidence" @click="closeNav">Evidence</a>
          <UButton class="button button-small button-dark" color="neutral" href="https://github.com/bpy-dev/blender-mcp">View source <span aria-hidden="true">↗</span></UButton>
        </nav>
      </div>
    </header>

    <main id="main-content">
      <section id="top" class="hero" aria-labelledby="hero-title">
        <div class="hero-grid" aria-hidden="true"><span /><span /><span /></div>
        <div class="shell hero-layout">
          <div class="hero-copy">
            <UBadge class="eyebrow" color="neutral" variant="subtle"><span class="status-dot" aria-hidden="true" /> Open community preview</UBadge>
            <h1 id="hero-title">Use Blender as a Python module. Give agents a narrow MCP interface.</h1>
            <p class="hero-lede">A focused path from ordinary Python code to Blender scenes: one runtime you can import, four tools an agent can reason about, and a protocol surface that stays still.</p>
            <div class="actions" role="group" aria-label="Project links">
              <UButton class="button button-primary" href="https://github.com/bpy-dev/blender-mcp">Explore blender-mcp <span aria-hidden="true">↗</span></UButton>
              <UButton class="button button-secondary" color="neutral" variant="outline" href="https://github.com/bpy-dev/blender-mcp/issues">Give feedback <span aria-hidden="true">→</span></UButton>
            </div>
            <p class="hero-note">Standalone bpy packaging remains work in progress. <a href="https://github.com/michaelgold/buildbpy/pull/9">Track build work in PR #9</a>.</p>
          </div>
          <UCard class="runtime-card" role="region" aria-label="Python example" :ui="{ body: 'p-0 sm:p-0' }">
            <div class="runtime-topbar"><span>scene.py</span><span>Python</span></div>
            <pre><code><span class="code-dim"># Blender, from Python</span>
<span class="code-key">import</span> bpy

cube = bpy.data.objects[<span class="code-string">"Cube"</span>]
cube.rotation_euler.z = <span class="code-num">0.785</span>

bpy.context.scene.render.filepath = <span class="code-string">"frame.png"</span>
bpy.ops.render.render(write_still=<span class="code-key">True</span>)</code></pre>
            <div class="runtime-status"><span><i aria-hidden="true" /> Local runtime</span><span>No application wrapper</span></div>
          </UCard>
        </div>
      </section>

      <section id="capabilities" class="capabilities rule-top" aria-labelledby="capabilities-title">
        <div class="shell">
          <div class="section-heading">
            <p class="kicker">01 / What developers can do</p>
            <h2 id="capabilities-title">Two surfaces. One Blender runtime.</h2>
            <p>Keep direct control in Python. Expose only the operations an agent needs.</p>
          </div>
          <div class="capability-grid">
            <UCard class="capability-card" as="article" :ui="{ body: 'contents' }">
              <span class="card-index" aria-hidden="true">A</span>
              <div><h3>Import Blender</h3><p>Build tools, render pipelines, tests, and batch jobs around <code>import bpy</code> in a normal Python workflow.</p></div>
              <span class="card-tag">Python API</span>
            </UCard>
            <UCard class="capability-card capability-card-dark" as="article" :ui="{ body: 'contents' }">
              <span class="card-index" aria-hidden="true">B</span>
              <div><h3>Constrain agents</h3><p>Give an agent exactly four MCP tools instead of a sprawling control plane. Smaller surfaces are easier to inspect and evaluate.</p></div>
              <a class="card-link" href="https://github.com/bpy-dev/blender-mcp">Inspect the interface <span aria-hidden="true">↗</span></a>
            </UCard>
          </div>
        </div>
      </section>

      <section id="architecture" class="architecture rule-top" aria-labelledby="architecture-title">
        <div class="shell architecture-layout">
          <div class="section-heading architecture-intro">
            <p class="kicker">02 / System boundary</p>
            <h2 id="architecture-title">Runtime → MCP → Frozen Protocol</h2>
            <p>Separate execution from agent access, then make the evaluation boundary repeatable.</p>
          </div>
          <ol class="architecture-flow">
            <li><span class="flow-number">01</span><div><h3>Runtime</h3><p>Blender capabilities available through Python, suitable for local tooling and automation.</p></div></li>
            <li><span class="flow-number">02</span><div><h3>MCP</h3><p>A narrow adapter: exactly four tools, explicit inputs, inspectable outputs.</p></div></li>
            <li><span class="flow-number">03</span><div><h3>Frozen Protocol</h3><p>Tasks, rounds, rendering, and scoring held constant for the reported run.</p></div></li>
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
