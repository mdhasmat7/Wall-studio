# Wall Studio

Reusable local interior visualization tool. Requires Node.js 22+; no npm packages or paid hosting required.

## Start

On this PC, right-click `Start-WallStudio.ps1` and select **Run with PowerShell**. Alternatively, open a terminal in this folder and run `node server.mjs`, then open http://127.0.0.1:4318.

1. Enter your existing OpenAI API key in the masked field in the app, never in chat.
2. Upload a moodboard, a floor plan labelled A–D, and 1–4 blank views facing the corresponding walls. Images: PNG, JPG or WebP, maximum 10 MB. Floor plans also accept PDF up to 20 MB; choose the desired page and check its preview.
3. Add optional design notes, select quality, and generate.
4. Switch between Original and Result, and download each finished PNG.

The first available finished view becomes an extra style reference for subsequent views. Each request includes the moodboard, selected floor-plan page, target blank view and any other uploaded views. The plan controls placement; the blank render controls camera and visible architecture. This encourages consistency but cannot guarantee exact geometry or identical furniture across views. These are concept visuals, not editable 3D scenes or construction drawings.

Each uploaded view uses one separate billable API request. Empty views are skipped. There are no automatic retries. On failure, completed views stay available; click Render on an individual wall to retry it or continue with other walls. A request that times out may still have been billed. Check API usage before retrying. Regenerating wall 1 does not automatically update other views; rerender those if needed.

Your key stays in browser memory and is passed through the loopback-only Node server to api.openai.com. The app does not save the key or images to disk, use localStorage, or log request bodies. Files and generated images are sent to OpenAI for generation. Browser extensions can access page contents according to their permissions. Refreshing or closing the page clears the session; download your images first.

API image access and billing must be enabled for your OpenAI project. Model access varies; choose another listed model if one is unavailable. Generation can take several minutes per view. Default output size is selected by the image API and might differ from the source dimensions.

The launcher keeps a local server running in the background. To stop it on Windows: find the PID with `Get-NetTCPConnection -LocalPort 4318 -State Listen`, verify it is the Wall Studio Node process, then use `Stop-Process -Id <PID>`. If started in a terminal, Ctrl+C stops it.

API contract: https://developers.openai.com/api/reference/resources/images/methods/edit

Validation: local server and request-building checks can run without API billing. Live generation requires your key and input images.

## PDF support

PDF pages are converted locally to PNG before generation; only the selected page is sent to OpenAI. The PDF itself is not uploaded to OpenAI. Conversion uses Python with pypdfium2 (available in this PC’s bundled Codex runtime). On another PC, install Python and run `python -m pip install pypdfium2 Pillow`, or use a PNG/JPG floor plan. Set WALL_STUDIO_PYTHON to a specific Python executable if needed. Password-protected or malformed PDFs may need to be exported as images. Check the preview for readable wall labels and dimensions.
