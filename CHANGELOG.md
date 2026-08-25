# Changelog

## [2.0.2] - 2026-08-25

### Fixed

- Pass the catalog query as keyword arguments. Passed positionally, the catalog's path-based check for "Access inactive portal content" did not see the path, so users holding the permission through a locally assigned role never got expired or not yet effective items in the context menu; with `collective.solr` installed the check was skipped entirely. @jmevissen

## [2.0.1] - 2026-03-24

### Fixed

- Show default value of show_in_contextmenu field in volto edit form as selected if default value is True. @jmevissen

## [2.0.0] - 2026-02-13

### Breaking changes

- Switch to implicit namespaces. @arybakov05


## [1.0.1]

- No significant changes.


## [1.0.0]

- Initial release. @jmevissen
