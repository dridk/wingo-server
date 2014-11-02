DEBUG           = True
SECRET_KEY      ="writeyourownsecretkey"
DATABASE        ="wingo"
VERSION         ="1.0"
VERSION_NAME    ="Xu Fu"
ALLOWED_RADIUS  = [100,500,1000,5000]
MAX_NOTE_LENGTH = 255
COUNT_PER_PAGE  = 20

CACHE_MAX_ITEM     = 500000 # Number of request that can be keep in cache at the same time
CACHE_MAX_DURATION = 5 * 60 # Delai in seconds before the expiration of a request in cache
CACHE_LOC_DELTA    = 50     # Distance max in meter to invalidate a cached request (if location shift more than CACHE_LOC_DELTA meters than the current location)