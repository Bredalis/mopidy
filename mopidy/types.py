from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypeVar, Union

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

F = TypeVar("F")
QueryValue: TypeAlias = Union[str, int]
Query: TypeAlias = dict[F, list[QueryValue]]

# Types for distinct queries
DistinctField: TypeAlias = Literal[
    "uri",
    "track_name",
    "album",
    "artist",
    "albumartist",
    "composer",
    "performer",
    "track_no",
    "genre",
    "date",
    "comment",
    "disc_no",
    "musicbrainz_albumid",
    "musicbrainz_artistid",
    "musicbrainz_trackid",
]
DistinctQuery: TypeAlias = dict[DistinctField, list[QueryValue]]

# Types for search queries
SearchField: TypeAlias = Union[DistinctField, Literal["any"]]
SearchQuery: TypeAlias = dict[SearchField, list[QueryValue]]

# Types for tracklist filtering
TracklistField: TypeAlias = Literal[
    "tlid",
    "uri",
    "name",
    "genre",
    "comment",
    "musicbrainz_id",
]

# Superset of all fields that can be used in a query
QueryField: TypeAlias = Union[DistinctField, SearchField, TracklistField]

# URI types
Uri: TypeAlias = str
UriScheme: TypeAlias = str
