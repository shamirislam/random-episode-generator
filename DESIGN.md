---
name: Random Episode Generator
description: A broadcast-continuity surface that announces one sitcom episode and hands over the next.
colors:
  ground: "#F1F3F5"
  panel: "#E3E7EB"
  rule: "#C6CCD3"
  tick: "#7E8894"
  fg: "#0B1219"
  fg-dim: "#59636F"
  on-ident: "#07101A"
  stage-black: "#000000"
  ident: "#FF4B12"
  ident-ink: "#B23107"
  ident-office: "#FF4B12"
  ident-office-ink: "#B23107"
  ident-friends: "#8B5CF6"
  ident-friends-ink: "#5B21B6"
  ident-bbt: "#00C2D1"
  ident-bbt-ink: "#046070"
typography:
  display:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "clamp(1.5rem, 2.9vw, 2.75rem)"
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: "-0.005em"
    fontVariation: "'wdth' 118"
  body:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.5
  quote:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.45
  action:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 700
    letterSpacing: "0.1em"
    fontVariation: "'wdth' 112"
  label:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "0.625rem"
    fontWeight: 600
    letterSpacing: "0.18em"
  label-station:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 600
    letterSpacing: "0.16em"
  numeric-lead:
    fontFamily: "Azeret Mono, ui-monospace, monospace"
    fontSize: "1.0625rem"
    fontWeight: 500
    lineHeight: 1.15
    fontFeature: "'tnum'"
  numeric:
    fontFamily: "Azeret Mono, ui-monospace, monospace"
    fontSize: "0.8125rem"
    fontWeight: 500
    letterSpacing: "0.06em"
    fontFeature: "'tnum'"
  numeric-micro:
    fontFamily: "Azeret Mono, ui-monospace, monospace"
    fontSize: "0.6875rem"
    fontWeight: 400
    letterSpacing: "0.05em"
    fontFeature: "'tnum'"
rounded:
  none: "0px"
  dot: "50%"
spacing:
  tight: "7px"
  snug: "12px"
  stack: "14px"
  seam: "16px"
  inset: "22px"
  meta: "30px"
  column: "40px"
  rail: "60px"
components:
  button-next:
    backgroundColor: "{colors.ident}"
    textColor: "{colors.on-ident}"
    typography: "{typography.action}"
    rounded: "{rounded.none}"
    padding: "17px 26px"
  lower-third-plate:
    backgroundColor: "{colors.ident}"
    textColor: "{colors.on-ident}"
    typography: "{typography.display}"
    rounded: "{rounded.none}"
    padding: "16px 28px 18px 22px"
  lower-third-channel:
    backgroundColor: "{colors.on-ident}"
    textColor: "{colors.ident-ink}"
    typography: "{typography.numeric-lead}"
    rounded: "{rounded.none}"
    padding: "18px 16px"
  station-bug-channel:
    backgroundColor: "{colors.ident}"
    textColor: "{colors.on-ident}"
    typography: "{typography.numeric}"
    rounded: "{rounded.none}"
    padding: "7px 10px"
  station-bug-name:
    backgroundColor: "transparent"
    textColor: "{colors.fg}"
    typography: "{typography.label-station}"
    rounded: "{rounded.none}"
    padding: "7px 14px"
  stage:
    backgroundColor: "{colors.stage-black}"
    rounded: "{rounded.none}"
    padding: "0px"
  key-cap:
    backgroundColor: "transparent"
    textColor: "{colors.fg}"
    typography: "{typography.numeric-micro}"
    rounded: "{rounded.none}"
    padding: "1px 5px"
---

# Design System: Random Episode Generator

## Overview

**Creative North Star: "The Continuity Booth"**

This is the room between programmes. Not the listings page, not the library, not the poster wall — the booth where the next thing is already cued and someone tells you what it is. Everything on the surface is furniture from that room, rendered as working chrome rather than decoration: a paper ground the colour of a lit studio wall, four safe-area brackets at the corners of the composition, a station bug carrying the channel number and the show's name, and a lower third that seats itself on the bottom-left of the still and announces the title. The still is the largest thing on screen because recognition is the fastest route to a yes.

The system's whole colour argument is the ident. Each show ships one saturated hue that fills complete rectangles — the title plate, the bug's channel chip, the NEXT button — and swaps in a single beat when the channel changes. It is never a tint, never a border, never a 4px underline. The rest of the palette is four steps of paper and two steps of ink, joined by 1px hairlines. There is no shadow anywhere in the build; depth is carried by the black stage well, the hairline, and the ident plate physically overlapping the image.

Density is high but not busy: on desktop the composition is exactly one viewport tall and never scrolls, which means every fact about the episode — title, season and episode, summary, quote, air date, rating, runtime — and the only control are all in view at once. Confirmed refusals, all visible in the build's own material: no gradient scrim under type, no rounded corners, no card that could be repeated into a grid, no second control, no cross-fade.

**Key Characteristics:**
- Ink ground, square corners, 1px hairlines, and not one shadow.
- One saturated ident per show, filling whole fields rather than accenting them.
- Expanded Archivo caps for the title; Azeret Mono for every number the interface states.
- Broadcast furniture as working chrome: safe-area brackets, station bug.
- A desktop frame locked to `100dvh` — the page never scrolls, the synopsis does.
- Cuts and slides only; content never cross-fades from old to new.
- Exactly one control, reachable by pointer or by `N` / `Space`.

## Colors

Four steps of near-white paper and two steps of near-black ink, interrupted by exactly one saturated hue that belongs to whichever show came up.

### Primary

The ident is a runtime slot, not a fixed value. `--ident` and `--ident-ink` are written onto `:root` by the server on first render and rewritten by the client on every draw, so the whole surface re-idents in one 260ms transition. Three pairs exist, one per show, and no fourth may be invented without a fourth show.

- **Broadcast Orange / Deep Orange** (`{colors.ident-office}` / `{colors.ident-office-ink}`): The Office, channel 01. Fills the title plate, the bug chip and the NEXT button; the darkened ink sets the small type and the ANNOUNCER tag.
- **Cathode Violet / Deep Violet** (`{colors.ident-friends}` / `{colors.ident-friends-ink}`): Friends, channel 02. Same two jobs.
- **Test-Card Cyan / Deep Cyan** (`{colors.ident-bbt}` / `{colors.ident-bbt-ink}`): The Big Bang Theory, channel 03. Same two jobs.
- **Ident Ink** (`{colors.on-ident}`): the near-black that sits *on* an ident field — the episode title on the plate, the label on the button, the channel number in the bug. It also backs the lower third's channel block, which is the one place the near-black becomes a field of its own.

### Neutral

- **Studio Ink** (`{colors.ground}`): the page ground. One field, uninterrupted, edge to edge.
- **Monitor Black** (`{colors.stage-black}`): the stage box behind the still, one step below the ground so the image reads as a lit screen inside a dark frame.
- **Rack Panel** (`{colors.panel}`): a single job — the scrollbar track. Declared as a token, but it has not earned promotion to a surface-layer scale; do not start layering panels on it without a reason.
- **Hairline** (`{colors.rule}`): every divider and every border in the system — the rail's underline, the stage frame, the bug's outline, the info section's top rule, the key-cap outline, the scrollbar thumb.
- **Tick Grey** (`{colors.tick}`): the four safe-area corner brackets only. Non-text, deliberately dim.
- **Broadcast White** (`{colors.fg}`): titles on the ground, synopsis body, meta values, the station name.
- **Muted Signal** (`{colors.fg-dim}`): the announcer quote, meta field labels, and the keyboard hint.

### Named Rules

**The Whole-Field Rule.** The ident colour fills a complete rectangle or it does not appear. Plate, channel chip, button — full backgrounds, no exceptions for borders, underlines, tints or icon strokes. Its only sub-field appearances are the text caret and the scrollbar thumb on hover, both of which are chrome, not content.

**The Two-Tint Rule.** Every show ships a pair. The saturated `--ident` only ever fills; the darkened `--ident-ink` only ever draws — small text and the focus ring — because it is the shade of that hue that clears 4.5:1 against the paper ground. Never set type in `--ident` on the ground; never fill a field with `--ident-ink`.

**The Black Well Rule.** The stage is `#000`, one step darker than the page. The still fills it edge to edge with `object-fit: cover` and no overlay, no scrim, no vignette, no colour grade.

## Typography

**Display Font:** Archivo (self-hosted variable WOFF2, `wght` 400–800, `wdth` 62–125; fallback `system-ui, sans-serif`)
**Body Font:** Archivo, same file
**Label/Mono Font:** Azeret Mono (self-hosted variable WOFF2, `wght` 400–500; fallback `ui-monospace, monospace`)

**Character:** Archivo pushed wide and heavy is a channel-ident face — the lettering of a title card, not of an article. Azeret Mono is the readout beside it: even, tabular, unhurried, the face of a timecode. The pairing splits the surface cleanly into things that are said and things that are measured. Both faces are preloaded and declared `font-display: block`; the width axis *is* the lettering here, so the surface waits for the file rather than flashing a platform sans and reflowing.

### Hierarchy

- **Display** (`{typography.display}`, uppercase, `text-wrap: balance`): the episode title on the ident plate, and nothing else. Words are wrapped in individual spans so they can rise in sequence on a channel change. Shrinks to `clamp(1.5rem, 6.6vw, 2.25rem)` under 900px and to `clamp(1.4rem, 2.3vw, 2.1rem)` on short desktop viewports.
- **Numeric Lead** (`{typography.numeric-lead}`): the season and episode stacked in the lower third's channel block — `S02` over `E14`, always zero-padded to two digits. Drops to `0.9375rem` under 900px.
- **Body** (`{typography.body}`, max `68ch`): the episode summary. `0.9375rem` under 900px.
- **Quote** (`{typography.quote}`, max `62ch`, in Muted Signal): the announcer's line.
- **Action** (`{typography.action}`, uppercase): the NEXT button label — the one place besides the title that touches the width axis.
- **Label Station** (`{typography.label-station}`, uppercase): the show name in the station bug.
- **Label** (`{typography.label}`, uppercase): field labels — FIRST AIRED, RATING, RUNTIME, ANNOUNCER. The wordmark sits one step up at `0.6875rem` on the same 0.18em tracking.
- **Numeric** (`{typography.numeric}`): the channel number in the bug, the season and episode, and every meta value.
- **Numeric Micro** (`{typography.numeric-micro}`): the keyboard hint and its key caps.

### Named Rules

**The Numbers Are Mono Rule.** Every number the interface states about the programme is Azeret Mono: the channel, the season and episode, the air date, the rating, the runtime, the key caps. Numerals inside prose and inside episode titles stay in Archivo, because there they are language, not data. `font-variant-numeric: tabular-nums` is set globally so a changing value never shifts its neighbours.

**The Width Axis Rule.** Emphasis comes from width before it comes from size. The title runs `wdth` 118 at weight 800; the button runs `wdth` 112 at weight 700. Nothing else in the system touches the axis — a new element gets emphasis from case and tracking, not by widening.

**The Caps-For-Chrome Rule.** Uppercase with 0.1–0.2em tracking is reserved for chrome: the title, the button, the station name, field labels, the wordmark. Body copy and the announcer quote are always sentence case and never tracked.

## Layout

The composition is a three-row grid inside a safe area. `.broadcast` is `height: 100dvh` with `padding: {spacing.inset}` and `grid-template-rows: {spacing.rail} minmax(46vh, 1fr) auto`, rows separated by `{spacing.stack}`. Four 16px L-brackets are absolutely positioned 8px from each viewport corner, marking the safe area the way a monitor's overlay would — built from a 1px `{colors.tick}` border with two sides removed, `pointer-events: none`.

**Row 1, the rail** (60px): the wordmark left and the station bug right, pushed apart with `justify-content: space-between` and closed by a 1px bottom hairline at 12px. The rail states what this is and what came up, and nothing else.

**Row 2, the programme**: the stage flexes to fill, framed by a 1px hairline over `#000`. The lower third is absolutely positioned at the stage's bottom-left, capped at `min(100%, 62ch)`, overlapping the image rather than sitting under it.

**Row 3, the information**: two columns, `minmax(0, 1fr) auto`, bottom-aligned with a `{spacing.column}` gap and a 1px top hairline at `{spacing.seam}`. Synopsis and quote left; the meta definition list, the NEXT button and the keyboard hint stacked right and right-aligned, with `{spacing.meta}` between meta fields.

The spacing rhythm is a loose 2px-resolution set rather than a strict 8pt grid; the reused steps are the ones in `spacing`, with control padding running on odd values (`17px 26px` on the button, `7px 10px` on the bug chip) because these are optical fits to type, not grid multiples.

**Responsive behaviour.** Three breakpoints, all of them changes of state rather than of identity:

- **≤900px**: `--rail` drops to 44px and `--inset` to 12px, the grid gap goes to 0 with `align-content: start`, and the page starts scrolling. The stage takes `aspect-ratio: 16 / 9` instead of flexing. The lower third leaves the image and becomes a static block directly beneath it, gaining a 1px hairline on three sides. The info column collapses to one column, the button goes full width, the wordmark steps down to 0.625rem, and the keyboard hint is hidden — it only makes sense with a keyboard.
- **≥901px and ≤820px tall**: the title's clamp tightens, the synopsis cap comes down to `6.4em`, and the lower third's padding contracts. The frame stays locked to the viewport.
- **≥901px and ≤640px tall**: the frame gives up its fixed height (`height: auto; min-height: 100dvh`), the page scrolls, and the synopsis cap is released.

### Named Rules

**The One Screen Rule.** On desktop the frame is exactly the viewport and `body` is `overflow: hidden`. Nothing is below the fold because there is no fold. A long summary scrolls inside its own block — `max-height: 8.6em`, `scrollbar-width: thin`, `overscroll-behavior: contain` — never by growing the page. If a new element cannot fit, something else has to shrink.

**The Safe Area Rule.** Content lives inside the 22px inset with the four brackets marking it. Nothing bleeds to the viewport edge; the only edge-to-edge surface is the still inside its own stage box.

## Elevation & Depth

There is not one `box-shadow` in this build, and there is no blur, no glass, no glow. Depth is carried by three moves and only three: a **1px `{colors.rule}` hairline** to separate one region from the next; the **black stage well**, which is one step darker than the page ground so the still reads as a lit panel recessed into it; and **overlap**, where the ident lower third physically sits on top of the image rather than beside it. Layering is tonal and structural, never atmospheric.

The single gradient in the system is transient and carries no content: the roll bar, a vertical white-alpha sweep (0 → 0.22 → 0) that crosses the stage once during a channel change and is `pointer-events: none` and `aria-hidden` throughout.

### Named Rules

**The No-Shadow Rule.** Surfaces do not float. If an element needs to read as above another, it overlaps it or it gets a hairline. Adding a shadow to this world puts it in a different one.

**The No-Scrim Rule.** Text over the still sits on a solid opaque bar. A gradient scrim, a darkened overlay or a blurred backdrop under type is out of the system — the lower third's legibility comes from the field, not from dimming the picture.

## Shapes

Every rectangle in the system is square. No element declares a `border-radius` anywhere. Borders are always exactly 1px and always `{colors.rule}`, so the whole surface is drawn with one weight of line; the only other stroke widths are the 2px focus ring and the 2.4px bar inside the NEXT glyph.

The recurring silhouette is the **stacked bar**: two flush rectangles of different fills sharing a full-height edge with no gap, no radius and no seam. It appears twice — the station bug (ident chip + outlined name) and the lower third (near-black channel block + ident plate) — and it is the shape a new composite element should reach for.

The safe-area brackets are the system's one open form: 16px squares with two adjacent borders removed, giving four corner marks that imply a frame without drawing one.

### Named Rules

**The Square Corner Rule.** Radius is 0px everywhere. The only curve permitted is a status dot.

## Components

Every component is either a fill or an outline; there is no third treatment. Fills are ident or near-black; outlines are the 1px hairline. Controls are blunt and confident — big targets, uppercase labels, no ornament.

### Buttons

- **Shape:** Hard square corners (0px), no border.
- **Primary (`button-next`)** — the only button in the system: an ident-filled block with a near-black uppercase label, padded wider than it is tall, `display: inline-flex` with a 12px gap to a 15×14 inline SVG next-track glyph (triangle plus bar) drawn in `currentColor`.
- **Hover:** `filter: brightness(1.12)` over 140ms — the fill brightens, the colour does not change.
- **Active:** `transform: translateY(1px)` — a 1px press, no scale.
- **Disabled / in progress:** `filter: brightness(0.72)` with `cursor: progress`, and the label swaps to "Tuning" for the duration of the draw.
- **Focus:** the global ring — 2px `{colors.ident-ink}` at `outline-offset: 3px`.
- **Mobile:** full width with a centred label.
- There is no secondary, ghost or tertiary variant, and adding one would break the surface's single-control premise.

### Station Bug

- **Style:** a stacked bar boxed in a 1px hairline. Left cell is the ident-filled channel chip (`CH 01`) in mono; right cell is the show name in tracked uppercase Archivo on transparent ground, `align-self: center`, truncating with an ellipsis rather than wrapping.
- **State:** the chip's `background` transitions over 260ms when the channel changes. On a failed draw the chip's text becomes `OFF AIR` and keeps the previous show's colour.
- **Mobile:** both cells drop to `0.625rem` with tighter 0.12em tracking.

### Lower Third (signature component)

The system's centrepiece. A stacked bar seated on the still's bottom-left, capped at `min(100%, 62ch)`.

- **Channel block:** near-black field, paper numerals, season over episode, both zero-padded to two digits.
- **Plate:** ident-filled, holding the episode title in near-black display caps, vertically centred, with asymmetric padding that gives the title more room on the right than on the left.
- **Retract:** on a draw it slides out left — `translateX(calc(-100% - 4px))` over 260ms — and slides back once the new still has cut in.
- **Mobile:** leaves the image entirely, becomes a static block beneath the stage, and picks up a hairline on left, right and bottom.

### Meta Block

- **Style:** a `<dl>` of three fields laid out as flex columns with a 30px gap. Label above value: tracked uppercase Archivo micro-caps in Muted Signal, mono value in Broadcast White at weight 500.
- **Empty state:** a missing rating or air date renders an em dash (`—`), never a blank or a zero.
- **Mobile:** wraps, gap narrows to 20px.

### Announcer Quote

- **Style:** an ident-ink uppercase label ("ANNOUNCER") on its own line above a sentence-case quote in Muted Signal, capped at 62ch. The label's colour transitions with the ident over 260ms.
- Labels attach to **data fields** in this system — this one and the three meta keys. A label never sits above the episode title.

### Key Cap

- **Style:** inline mono text in a 1px hairline box at `1px 5px`, no fill, no radius, inside the keyboard hint line. Hidden under 900px.


### Channel Change (signature transition)

The one composed motion in the system, orchestrated in JS around a single easing token, `cubic-bezier(0.16, 1, 0.3, 1)`:

1. The button disables and its label becomes "Tuning".
2. The lower third retracts left (260ms).
3. The next still is fetched and decoded — `img.decode()` — in parallel with a 200ms floor, so the cut can only land on a frame that is ready.
4. The roll bar sweeps the stage once (520ms linear), and 190ms in, everything repaints at once under it: still, ident variables, channel, bug, title, synopsis, quote, meta.
5. The lower third slides back and the title's words rise in sequence — `translateY(0.42em)` to 0 with opacity, 420ms each, staggered 45ms per word.
6. A visually-hidden live region announces "Now showing: …".

Under `prefers-reduced-motion: reduce` the sequence collapses to decode-then-paint: the roll animation, every 260ms transition and the word-rise are all switched off, and the swap is instantaneous.

### Off Air (error state)

A failed draw never empties the screen. The current still, title, meta and quote stay exactly as they are; the lower third and roll are reset; the bug chip relabels to `OFF AIR`; the button re-enables reading "Signal lost — try again"; and the live region says the episode on screen has not changed.

### Named Rules

**The One Control Rule.** The surface has exactly one interactive element, and it is the only ident-filled thing below the stage. It is bound to `N` and `Space` as well as to click, and it is never scrolled out of reach.

**The Cut, Never Fade Rule.** Content changes are cuts and slides. Nothing cross-fades from old content to new — a fade would show two programmes at once, which is the one thing this world will not do. Colour and the roll sweep may transition; text and images may not.

**The Kept Programme Rule.** No state — loading, error, or draw-in-flight — is allowed to blank the stage. What is on air stays on air until something better has fully arrived.

## Do's and Don'ts

### Do:

- **Do** fill a complete rectangle with the ident colour or leave it out entirely — plate, channel chip, button. See **The Whole-Field Rule**.
- **Do** use the paired `--ident-ink` tint whenever that hue has to become type on the paper ground, and keep near-black `{colors.on-ident}` for type on an ident field.
- **Do** set every stated number in Azeret Mono and every word in Archivo, per **The Numbers Are Mono Rule**.
- **Do** reach for the width axis before size when a new element needs emphasis (`wdth` 118 / 800 for display, 112 / 700 for actions).
- **Do** separate regions with a single 1px `{colors.rule}` hairline, the system's only line weight.
- **Do** keep the desktop composition inside `100dvh` and let long text scroll inside its own block.
- **Do** gate a still swap on `img.decode()` so the cut lands on a decoded frame, and keep the roll sweep over the moment of the cut.
- **Do** give every new focusable the 2px `{colors.ident-ink}` ring at `outline-offset: 3px`.
- **Do** render a missing value as an em dash and keep the field visible.
- **Do** hide the keyboard hint under 900px rather than shrinking it further.

### Don't:

- **Don't** set type in `--ident` on the paper ground, or fill a field with `--ident-ink`. The two tints do not swap jobs.
- **Don't** put a gradient scrim, dark overlay or backdrop blur under text on the still — the lower third is a solid bar. The only gradient in the system is the transient roll sweep, which never carries content.
- **Don't** round a corner. Radius is 0px; the one circle is the 7px status dot.
- **Don't** add a `box-shadow`, glow or blur. Depth is hairline, black well and overlap.
- **Don't** cross-fade content, and don't animate the still's opacity. Changes cut or slide.
- **Don't** place a label, kicker or eyebrow above the episode title; its only companion is the S/E block beside it.
- **Don't** introduce a second control, or a second ident-filled element that competes with NEXT below the stage.
- **Don't** add a repeatable card, grid, rail or carousel of stills. There is no card component in this system, and the world refuses the library it would build.
- **Don't** let the type fall back to a platform sans — both faces are self-hosted, preloaded and `font-display: block` on purpose.
- **Don't** invent a fourth ident colour. Ident pairs come from the show table in `main.py`; a new colour means a new show.
