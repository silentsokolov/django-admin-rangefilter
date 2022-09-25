## [Unreleased]

## [0.9.0] - 2022-09-25
### Added
- Add filter for integer and float #85

## [0.8.8] - 2022-09-01
### Fix
- Fix using settings.USE_TZ = False on django4.0+ #85

## [0.8.7] - 2022-08-13
### Added
- Use admin CSS vars for colors (thx @mharju)
- Added Farsi translation (thx @shahmohammadims)

## [0.8.6] - 2022-08-07
### Added
- Compatibility Django 4.1

## [0.8.5] - 2022-07-03
### Fix
- Fix use of admin_static causes validate_templates fails #78

## [0.8.4] - 2022-02-19
### Fix
- `nonce` breaks admin inlines styles #74 (thx @fabiocaccamo)
- Fix tests

## [0.8.3] - 2021-12-19
### Added
- Compatibility Django 4.0

## [0.8.2] - 2021-10-31
### Fix
- Fixing case with two widgets on one page #67 (thx @snnwolf)

## [0.8.1] - 2021-08-10
### Fix
- Fixed problem with `ManifestStaticFilesStorage` #63

## [0.8.0] - 2021-04-10
### Added
- Compatibility Django 3.2

### Changed
- Module `filter` rename to `filters`

### Fix
- Fixed static loads

## [0.7.0] - 2021-02-22
### Added
- Added possibility to set a title of filter #58

### Fix
- Avoided leading ?& GET parameters #59 (thx @jaredahern)

### Changed
- Changed title of filter from `By {field_name}` to `{field_name}`

## [0.6.4] - 2021-01-19
### Added
- Added Greek translation
- Added Italian translation
- Moved tests to Github Actions

## [0.6.3] - 2020-10-01
### Added
- Added Polish translation #45 (thx @sqlmiles)
- Added Japanese translation

### Fix
- Fix Portuguese translation #53

## [0.6.2] - 2020-08-07
### Added
- Compatibility Django 3.1

## [0.6.1] - 2020-06-05
### Added
- Added Danish translation #45 (thx @tiktuk)

### Changed
- Refactor tests

## [0.6.0] - 2020-05-04
### Added
- Added setter for initial field value (#44)

## [0.5.4] - 2020-02-10
### Added
- Added Simplified Chinese translation (thx @daimon99)

## [0.5.3] - 2019-12-16
### Added
- Added Brazilian portuguese translation (thx @sandrofolk)
- Use proper Template comment tag #39 (thx @nitinnain)

## [0.5.2] - 2019-12-04
### Added
- Compatibility Django 3.0

## [0.5.1] - 2019-10-15
### Changed
- Fix inline CSS that overrided base a admin CSS (#36)

## [0.5.0] - 2019-07-04
### Added
- Add csp compliance through django-csp (thanks @jsumnerPhD)

### Fixed
- Fix problem with locale

## [0.4.0] - 2019-04-19
### Changed
- Changed name lookup field `{field}__gte` -> `{field}__range__gte`
- Changed name lookup field `{field}__lte` -> `{field}__range__lte`

## [0.3.16] - 2019-04-14
### Changed
- Fix problem when thousand separator is used (#18)

## [0.3.15] - 2019-04-05
### Added
- Added Spanish translation
- Compatibility Django 2.2

## [0.3.14] - 2019-03-25
### Added
- Added French translation
- Added German translation

## [0.3.13] - 2019-03-21
### Added
- Added Czech translation

## [0.3.12] - 2019-01-31
### Added
- Added Russian translation

## [0.3.11] - 2019-01-30
### Changed
- Avoid loading admin_static in templates under Django>=1.10 (#27)

## [0.3.10] - 2018-12-05
### Changed
- Fix calendar position on mobile (#23)

## [0.3.9] - 2018-10-31
### Changed
- Fix calendar icons displayed for Django 2.1

## [0.3.8] - 2018-10-12
### Added
- Compatibility Django 2.1

## [0.3.7] - 2018-06-29
### Changed
- Fix system name with non-unicode char (#18)

## [0.3.6] - 2018-04-27
### Changed
- Change padding on the buttons (#16)

## [0.3.5] - 2018-03-17
### Added
- Compatibility Django 2.0

## [0.3.4] - 2018-03-17
### Changed
- Add get_timezone
- Drop support Django < 1.8

[Unreleased]: https://github.com/silentsokolov/django-admin-rangefilter/compare/0.9.0...HEAD
[0.9.0]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.8.8...v0.9.0
[0.8.8]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.8.7...v0.8.8
[0.8.7]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.8.6...v0.8.7
[0.8.6]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.8.5...v0.8.6
[0.8.5]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.8.4...v0.8.5
[0.8.4]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.8.3...v0.8.4
[0.8.3]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.8.2...v0.8.3
[0.8.2]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.8.1...v0.8.2
[0.8.1]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.8.0...v0.8.1
[0.8.0]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.6.4...v0.7.0
[0.6.4]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.6.3...v0.6.4
[0.6.3]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.6.2...v0.6.3
[0.6.2]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.5.4...v0.6.0
[0.5.4]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.5.3...v0.5.4
[0.5.3]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.5.2...v0.5.3
[0.5.2]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.16...v0.4.0
[0.3.16]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.15...v0.3.16
[0.3.15]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.14...v0.3.15
[0.3.14]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.13...v0.3.14
[0.3.13]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.12...v0.3.13
[0.3.12]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.11...v0.3.12
[0.3.11]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.10...v0.3.11
[0.3.10]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.9...v0.3.10
[0.3.9]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.8...v0.3.9
[0.3.8]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.7...v0.3.8
[0.3.7]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.6...v0.3.7
[0.3.6]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.5...v0.3.6
[0.3.5]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.4...v0.3.5
[0.3.4]: https://github.com/silentsokolov/django-admin-rangefilter/compare/v0.3.3...v0.3.4
