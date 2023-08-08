import logging
from pathlib import Path
from typing import cast

import mopidy
from mopidy import config, exceptions, ext

logger = logging.getLogger(__name__)


class Extension(ext.Extension):
    dist_name = "Mopidy-HTTP"
    ext_name = "http"
    version = mopidy.__version__

    def get_default_config(self):
        return config.read(Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        schema["hostname"] = config.Hostname()
        schema["port"] = config.Port()
        schema["static_dir"] = config.Deprecated()
        schema["zeroconf"] = config.String(optional=True)
        schema["allowed_origins"] = config.List(
            optional=True,
            unique=True,
            subtype=config.String(transformer=lambda x: x.lower()),
        )
        schema["csrf_protection"] = config.Boolean(optional=True)
        schema["default_app"] = config.String(optional=True)
        return schema

    def validate_environment(self):
        try:
            import tornado.web  # noqa: F401 (Imported to test if available)
        except ImportError as exc:
            raise exceptions.ExtensionError("tornado library not found") from exc

    def setup(self, registry):
        from .actor import HttpApp, HttpFrontend, HttpStatic
        from .handlers import make_mopidy_app_factory

        HttpFrontend.apps = cast(list[HttpApp], registry["http:app"])
        HttpFrontend.statics = cast(list[HttpStatic], registry["http:static"])

        registry.add("frontend", HttpFrontend)
        registry.add(
            "http:app",
            {
                "name": "mopidy",
                "factory": make_mopidy_app_factory(
                    registry["http:app"], registry["http:static"]
                ),
            },
        )
