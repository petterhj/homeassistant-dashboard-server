## ?.?.?

- Component type is now shown on cards when in error state.
- Bumped dependencies and reworked linting regime.
- Improved error handling for calendar data.

## 0.4.0

- Added tile card for single entities.
- Tolerate empty configuration file.
- Tolerate trailing slash in configured Home Assistant URL.
- Ignore events returned correctly from the Home Assistant API.
- Upgraded dependencies.

## 0.3.2

- Weather graph labels are now shown above annotation lines.

## 0.3.1

- Overflowing cards are now faded towards the bottom.
- Calendar cards can now be configured to display a limited amount of events.
- The margin of list card items (list, calendar, todo) have been reduced.
- The Y axis in the temperature graph are now padded by 10%.

## 0.3.0

- Fixed docker build.
- Upgraded to Playwright 1.41.0.
- Error card should now be rendered without a blue border.
- Fixed overlapping graph labels after building by specifying `LabelLayout` in
  order to prevent unwanted tree-shaking.

## 0.2.3

- Removed dependency on daisyUI.
- Upgraded dependencies.

## 0.2.2

- Added current version to dashboard footer.
- Frontend `package*.json` files are now also version bumped.

## 0.2.1

- Added a CHANGELOG and configured `bump2version` in order to keep track of
  changes.
