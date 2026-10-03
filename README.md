# android-compat-kb

What an Android code change can run into on other OS versions, device types and vendor ROMs — as data, each entry
with the source it comes from.

[mobile-dev-harness](https://github.com/mobile-dev-harness/mobile-dev-harness) reads it to turn a change into
compatibility risks (`mdh compat risks`): a new `SDK_INT` branch, a call whose behavior changed in API 34, a raised
`targetSdk`, a `layout-sw600dp`, background work that vendor battery managers kill. Other tools are welcome to use
it too.

## What's in it

[`android.yaml`](android.yaml) has three sections:

| Section | An entry says | Example |
|---|---|---|
| `behavior` | An Android behavior change: the first API level with it, whether it applies by the device's version or the app's `targetSdk`, what makes code run into it, what to verify | `pending-intent-mutability`: API 31, by target, `PendingIntent.getActivity` … |
| `form_factors` | What makes a change risky on another kind of device, and where to check it (a compact phone, landscape, a foldable's inner screen, a tablet) or what device it needs | `large-screen-resources`: `sw600dp` qualifiers → tablet |
| `vendors` | A vendor ROM quirk: the manufacturers, what triggers it, how it shows | `background-restrictions`: xiaomi, oppo, vivo, … `WorkManager` … |

Triggers, any of which matches:

- `uses`: names a changed declaration calls, references or overrides. `Type.name` matches a call on a receiver of
  that type, a bare `name` any use.
- `manifest`: manifest elements (`<service>`) or attributes (`screenOrientation`) the change adds or modifies.
- `qualifiers`: resource qualifiers (`sw600dp` matches `layout-sw600dp-land`).
- `features`: `<uses-feature>` names.

Other fields: `id` (stable, kebab-case), `summary` (what goes wrong, one line), `verify` (what to look at),
`source` (an https link, Android documentation where there is one), and per section `api`, `by`, `both_sides`;
`cells`, `state`, `needs`; `vendors`.

## Using it

Each release attaches `android.yaml` and its SHA-256:

```sh
curl -LO https://github.com/mobile-dev-harness/android-compat-kb/releases/download/v1.0.0/android.yaml
curl -L https://github.com/mobile-dev-harness/android-compat-kb/releases/download/v1.0.0/android.yaml.sha256 | sha256sum -c
```

Pin a version: matching is by name, so an entry that changes can change what a tool reports. mdh vendors a pinned
release (`crates/mdh-compat/kb/`); to try entries before a release, point it at a file with
`MDH_COMPAT_KB=/path/to/android.yaml`.

## Contributing

New entries and fixes are very welcome, especially vendor quirks seen on real devices. See
[CONTRIBUTING.md](CONTRIBUTING.md); `python3 scripts/validate.py` checks the format.

## License

MIT or Apache-2.0, at your option.
