# Talk to Revity: 1.0 preview

This preview runs **Qwen3-0.6B**, not the planned 480B model. It packages original
Qwen weights with a Revity interface; it is not a newly trained model. The small
model can be inaccurate and its answers are not benchmark claims.

## Install

Use Python 3.12 and allow approximately 8 GB free RAM and 5 GB free disk for
installation and inference. CPU operation was tested on Linux; other platforms
have not been verified. No GPU is required. Initial dependency/model downloads
need Internet access; inference uses local files only.

Extract the release ZIP and open a terminal in its directory. On Linux/macOS:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
```

On Windows, use `python -m venv .venv` and `.venv\Scripts\activate` instead of the
first two lines, then run the same pip commands. Windows is not yet tested.

The current draft has no bundled weights: downloads are blocked in the build
environment. From a computer with Hugging Face CDN access, download the pinned
weights first:

```sh
python scripts/download_model.py
```

## Browser chat

```sh
python -m revity.server
```

Wait for the ready message, then enter `http://127.0.0.1:7860` in a browser **on
the same computer running the server**. The server binds only to loopback; this
is not a hosted demo or a public deployment. Stop it with Ctrl+C.

The UI includes conversation history and New chat. CPU responses may take several
seconds. The server is single-user and processes one request at a time. It does
not save conversations to disk. Chat is limited to 4096 input tokens and 256
output tokens per browser request; long answers may be cut short. Start a new
chat if the context limit is reached. Model thinking mode is disabled for this
small CPU preview; it does not expose a reasoning trace.

## Terminal chat

```sh
python -m revity.chat
python -m revity.chat --prompt "Explain what a solar panel does in two sentences."
```

Use `/reset` to clear history and `/quit` to exit interactive chat.

## Verify

```sh
python -m unittest discover -s tests -v
```

Software tests use a fake model for HTTP routing checks. Real inference is currently blocked by model download access;
`docs/SMOKE_RESULTS.json` records that status, not successful model responses.
After downloading, run `python scripts/smoke_chat.py` to record three actual
responses. Those are functional checks, not a general model benchmark. The dataset scorer remains
available for independent evaluation; no full dataset evaluation is claimed.

Release assets have not yet been uploaded. Qwen license and attribution are included
under `third_party/` and in the model directory.
