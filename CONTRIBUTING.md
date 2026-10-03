# Contributing

An entry is only as good as the risk reports it leads to: a missed risk is a bug that ships, a wrong one costs a
developer a check for nothing. So:

- **Every entry needs a source.** Android documentation (developer.android.com) for behavior changes; for vendor
  quirks the vendor's documentation, an issue tracker, or a reproducible report (dontkillmyapp.com collects many).
  Say in the pull request which devices and ROM versions you saw it on.
- **Keep triggers specific.** Matching is by name: a common name (`enqueue`, `File`, `start`) matches unrelated
  code. Prefer the API's own names (`setExactAndAllowWhileIdle`, `PendingIntent.getActivity`); use `Type.name`
  when the bare name is ambiguous.
- **Say what to verify**, in a sentence a tester (or an agent) can act on: what to do, on which version or device,
  and what should happen.
- **Ids are stable.** Tools and reports refer to them; rename only with a major version.
- Run `python3 scripts/validate.py` before opening the pull request (it needs PyYAML).

Releases: entries land on `main`; a tag `vX.Y.Z` with a CHANGELOG section publishes `android.yaml` and its
SHA-256.
