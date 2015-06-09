from invenio.base.bundles import styles as _styles

_styles.contents.remove("less/base.less")
_styles.contents += ("less/cds.less",)
_styles.contents += ("less/experiments.less",)
