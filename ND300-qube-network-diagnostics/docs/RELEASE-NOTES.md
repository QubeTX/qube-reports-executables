# ND-300 4.0.1 — SpeedQX Methodology v5

Both nd300's embedded speed test and the standalone speedqx command now use Methodology 5.0. Headlines describe sustained application throughput: confirmed payload bytes divided by measured time, including slow stretches and stalls.

- Quick is the default across the CLI, website and app. Deep repeats the primary comparison and adds supporting measurements.
- Cloudflare and consenting M-Lab MSAK each contribute one primary-network result. NDT7 stays separately labeled single-stream evidence; supporting providers cannot silently raise the headline.
- Estimated ceilings require repeated, non-overlapping windows and are withheld when unsupported or below sustained speed. Result details expose variation and disagreement without a calibrated 95% accuracy claim.
- Idle HTTP RTT, download-loaded/upload-loaded RTT, probe failures and server TCP signals have distinct labels. Unmeasured packet loss stays unavailable.
- Synthetic payload limits, explicit M-Lab publication consent and owned cancellation preserve qualifying partial results. New CLI controls include --deep, --max-bytes and --accept-mlab. ND300 --fast still skips speed testing.

The matching [SpeedQX website](https://speedqx.com) uses the shared v5 engine and cassette instrument. iOS 3.0.0 (16) has been uploaded to App Store Connect; this is not an announcement of public App Store availability.

## Publication repair

The initial 4.0.0 crate attempt stopped before publication because its floating publisher toolchain selected a newer Clippy than CI. No 4.0.0 tag or release was created. Version 4.0.1 pins the publisher to the validated Rust 1.97.0 toolchain and applies an equivalent expression cleanup without changing the statistics arithmetic.

## Validation and limits

332 Rust tests, 90 website tests, 38 app tests and full parity across 88 traces passed. Native UI fixtures passed 30 first-attempt journeys across four iPhone sizes and Android. The independent security review found no Critical/High issues and records Medium/Low hardening follow-ups.

Publication was authorized with known limits: physical-device accessibility/lifecycle/animation acceptance and real-provider qualification remain open. Independent packet-loss comparisons missed the repeatability target, with retained optimized-run median differences of 35.11% download and 11.95% upload. The evidence does not establish physical line capacity or universal device accuracy. [Validation evidence](https://github.com/QubeTX/speedtest/blob/19c83fa484cb65ba4d529d48cc5966cdd106f416/evidence/v5/README.md), [security review](https://github.com/QubeTX/qube-network-diagnostics/blob/main/docs/evidence/v5/security-review.md).

The release provides both binaries across six platform targets, four Windows installer editions/channels, and a signed/notarized universal macOS package with a compatibility DMG for older updaters. Choose the installer matching your existing installation channel.


Complete [publication and deployment evidence](https://github.com/QubeTX/qube-network-diagnostics/blob/main/docs/release-evidence-v4.0.1.md), including exact workflow jobs, public asset hashes and App Store Connect delivery.

