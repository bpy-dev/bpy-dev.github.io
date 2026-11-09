# bpy.dev project plan

## Authority and scope

This is the whole-project plan for bpy.dev: its website, enhanced Blender MCP
runtime, standalone `bpy` build/packaging, and planned Hermes integration.
Component installation guides and technical checklists remain in their owning
repositories; they are not competing whole-project plans. This document separates
existing source from intended product capabilities. Publishing it does not ship a
plugin, certify a runtime, or launch a hosted service.

## Confirmed product direction

- Build a Hermes plugin exposing **the full enhanced Blender MCP capability
  surface**, not a reduced create/edit/render/export subset.
- Support **local `bpy` execution without a cloud subscription**.
- Support **paid cloud execution through Fstack**, with API-key / OAuth-login
  access. Detailed authentication flows and commercial terms remain to be designed.
- Preserve authentication, tenant isolation, and execution security boundaries.
  Full capability access is not unrestricted access to other users' data or hosts.

## Components and existing evidence

The following is a source-inspection baseline, not fresh end-to-end execution
acceptance. Links pin the inspected revisions so later changes are distinguishable.

| Component | Existing source and boundary |
| --- | --- |
| [Website](https://github.com/bpy-dev/bpy-dev.github.io) | Nuxt homepage, benchmark presentation, and static-site validation/deployment workflow. [README at `22efe60`](https://github.com/bpy-dev/bpy-dev.github.io/blob/22efe60b0e42f9cc160a9ac3efd9dd2c8e69413c/README.md). A website build does not establish runtime or hosted-product readiness. |
| [Enhanced Blender MCP](https://github.com/bpy-dev/blender-mcp) | Developer-preview source retains live add-on/server tools and adds saved-file subprocess execution, Blender executable or standalone `bpy` backend selection, runtime Python API lookup, and benchmark tooling. [Overview at `e8ac408`](https://github.com/bpy-dev/blender-mcp/blob/e8ac4088d4a3e0469d3eff9f9bb2dd717e899219/readme.md). These are existing runtime components, not evidence of a delivered Hermes plugin or cloud parity. |
| [buildbpy](https://github.com/michaelgold/buildbpy) | Standalone Blender Python build and packaging tooling, including documented ARM64 dependency-bundle verification and native-build fallback. [README at `8113295`](https://github.com/michaelgold/buildbpy/blob/8113295240b0d95781fa4c043b6cfecba9a6eba7/README.md). Availability and GPU support must be verified for each selected version/platform; this plan does not certify every advertised combination. |
| Fstack integration | Confirmed destination for the planned paid execution mode. This plan defines the bpy.dev integration goal, not Fstack's implementation status or deployment architecture. |

The enhanced MCP's [tool reference](https://github.com/bpy-dev/blender-mcp/blob/e8ac4088d4a3e0469d3eff9f9bb2dd717e899219/readme_tools.rst)
includes code execution, blend-file inspection, object summaries, bundled and
runtime API documentation, manual search, screenshots, workspace/viewport
navigation, and rendering. That reference and the selected runtime's actual
registered capabilities—not a hand-picked subset here—are the inventory for
plugin acceptance.

Live-session tools require a connected Blender add-on/session. Saved-file
`_for_cli` tools use fresh subprocesses; selecting standalone `bpy` does not turn
it into an interactive Blender UI. See the
[backend guide](https://github.com/bpy-dev/blender-mcp/blob/e8ac4088d4a3e0469d3eff9f9bb2dd717e899219/readme_bpy_backend.rst).
The integration must make these prerequisites explicit rather than silently
omit tools or claim headless execution supports UI-only behavior.

Existing benchmark artifacts are bounded evidence, not general product acceptance.
The website's linked BlenderBench compilation labels CLIP image-embedding cosine
similarity as “CLIP accuracy”; this is **not literal task accuracy**. Keep benchmark
methodology, attribution, and limitations alongside results.

## Planned delivery and acceptance

All items below remain open acceptance work for this product direction. Their
order describes dependencies, not promised dates or a reduced release scope.

### 1. Establish the full integration contract

- Pin the enhanced MCP revision and inventory its registered tools and any exposed
  resources/prompts. Define how Hermes discovers and accesses the entire surface.
- Record each capability's live-session, saved-file, runtime, and permission
  prerequisites. Explicitly design how local and hosted modes satisfy them,
  including tools that require a live UI/session; do not hide unresolved gaps.
- Define compatibility checks, installation/configuration, error reporting, and
  artifact handling. Acceptance requires a traceable capability matrix against
  the pinned runtime, not only a successful connection or sample render.

### 2. Deliver the local Hermes plugin path

- Provide installation and mode selection for local execution, including the
  standalone `bpy` path and documented live-session prerequisites where needed.
- Demonstrate operation with no cloud account, paid key, or cloud subscription.
- Exercise the full applicable capability inventory through Hermes, preserve
  tool schemas/results, and report unmet prerequisites explicitly. Test failures,
  timeouts, output handling, and safe source-file treatment as well as success.

### 3. Deliver paid execution through Fstack

- Specify and implement API-key / OAuth-login access and the boundary between
  the plugin, Fstack, and the Blender runtime. Credential lifecycle, entitlement,
  and account/session behavior require explicit design and tests.
- Establish tenant-isolated execution and artifact access, resource limits,
  cancellation/timeout behavior, and recovery from failed or interrupted work.
- Verify capability parity against the same inventory, including an explicit
  resolution for live-session tools. A headless-only smoke test cannot certify
  full enhanced MCP access.
- Verify authorized execution and result retrieval through Hermes, rejection of
  unauthorized/expired access, cross-tenant denial, and the paid-access boundary.
  Do not describe billing or hosted operation as accepted until exercised.

### 4. Publish evidence and reconcile component documentation

- Publish reproducible installation and acceptance instructions tied to exact
  runtime/plugin revisions and tested Blender/`bpy` versions and platforms.
- Reconcile the runtime's historical
  [publication checklist](https://github.com/bpy-dev/blender-mcp/blob/e8ac4088d4a3e0469d3eff9f9bb2dd717e899219/PUBLICATION_CHECKLIST.md)
  with current evidence: it still contains pre-publication wording although the
  repository is public. Do not treat checked historical gates as fresh tests or
  unchecked historical entries as proof that their outcomes never happened.
- Keep website claims aligned with verified local and hosted capabilities.
  Distinguish source publication, CI success, deployment, and end-to-end acceptance.

## Security and unresolved decisions

The existing [security model](https://github.com/bpy-dev/blender-mcp/blob/e8ac4088d4a3e0469d3eff9f9bb2dd717e899219/SECURITY.md)
permits powerful Blender Python execution. Fresh subprocesses provide process/state
isolation, **not an OS sandbox**. Hosted execution needs a separately verified
security boundary; local operation must document filesystem/network permissions
and protect credentials and unrelated files.

Open decisions include plugin packaging/distribution, the supported runtime and
platform matrix, live-session provisioning in hosted mode, authentication flow
and credential storage, entitlement/billing behavior, and artifact lifecycle.
No prices, launch dates, infrastructure providers, or deployment topology are
selected by this plan.

This document does not authorize implementation or deployment by itself. Changes
to the plugin/runtime and Fstack require their own reviewed work; benchmark work
and packaging fixes do not substitute for full integration acceptance.
