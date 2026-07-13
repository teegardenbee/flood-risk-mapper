"""
Seed dataset for Bengaluru flood-risk localities.

This module is the current stand-in for what will eventually be a proper
data layer (PostGIS tables + zonal statistics pulled from satellite and
rainfall rasters). Every locality has four *risk sub-scores* (0-100, higher
is worse) that feed the weighted composite score:

    elevation   -- low-lying terrain relative to surrounding wards
    drainage    -- proximity to encroached / silted stormwater drains (rajakaluves)
    lakebed     -- built on or adjacent to a historically filled lake/tank bed
    density     -- population & structures exposed per sq. km

IMPORTANT: these numbers are illustrative estimates derived from public
reporting patterns (BBMP flood-prone-spot lists, lake encroachment
coverage, drainage news), NOT verified official measurements. Treat this
as a prototyping dataset until it's replaced by the real pipeline
described in docs/architecture.md.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Locality:
    name: str
    lat: float
    lng: float
    elevation: int
    drainage: int
    lakebed: int
    density: int
    note: str


LOCALITIES: list[Locality] = [
    Locality("Bellandur", 12.9304, 77.6784, 88, 92, 95, 80,
             "ORR East service roads, chronic lake overflow"),
    Locality("Mahadevapura", 12.9591, 77.6974, 82, 88, 85, 75,
             "Interior pockets near old tank chain"),
    Locality("KR Puram", 13.0059, 77.6961, 80, 85, 78, 82,
             "Interior wards, Hebbal valley outflow"),
    Locality("HSR Layout", 12.9121, 77.6446, 75, 80, 90, 85,
             "Extension wards on former lake beds"),
    Locality("Whitefield-Hoskote corridor", 12.9698, 77.7500, 78, 82, 70, 68,
             "Low-lying arterial stretches"),
    Locality("Silk Board / BTM", 12.9166, 77.6228, 70, 78, 55, 90,
             "High density chokepoint"),
    Locality("Sarjapur Road", 12.9004, 77.6870, 72, 75, 65, 78,
             "110 villages belt, drains lag construction"),
    Locality("Koramangala", 12.9352, 77.6146, 65, 70, 60, 88,
             "Koramangala-Challaghatta valley floor"),
    Locality("Electronic City", 12.8452, 77.6602, 55, 60, 30, 65,
             "Improving but some low-lying pockets"),
    Locality("Jayanagar", 12.9308, 77.5838, 50, 55, 35, 70,
             "Older, moderately maintained drains"),
    Locality("Hebbal", 13.0358, 77.5970, 48, 50, 60, 60,
             "Near lake, infra upgraded post-2022"),
    Locality("Yelahanka", 13.1007, 77.5963, 35, 40, 30, 45,
             "North of airport corridor, lower risk"),
    Locality("Indiranagar", 12.9719, 77.6412, 30, 35, 20, 75,
             "Central, well above valley floor"),
    Locality("Malleshwaram", 13.0035, 77.5709, 28, 30, 15, 65,
             "Older well-drained layout"),
    Locality("Rajajinagar", 12.9991, 77.5554, 32, 38, 25, 60,
             "Generally stable drainage"),
]


def load_localities() -> list[Locality]:
    """Return the current locality dataset.

    Swap point: replace this with a call into the data layer, e.g.
        gdf = geopandas.read_postgis("SELECT * FROM localities", engine)
    once PostGIS is wired up (see docs/architecture.md).
    """
    return LOCALITIES
