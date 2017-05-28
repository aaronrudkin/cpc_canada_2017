library(raster) # Merging
library(rgeos) # Clip the shapefile
library(rgdal) # Shapefile
library(leaflet) # Plot map
library(mapview) # Save map
library(stringi) # Drop accents

# Read shapefile (shapefile from Elections Canada)
canada = readOGR("shapefile/FED_CA_2_2_ENG.shp")
canada = spTransform(canada, CRS("+proj=longlat +datum=WGS84 +no_defs"))

# Clip the northern territories a little bit
clip_box = as(raster::extent(-180, 0, 35, 70), "SpatialPolygons")
proj4string(clip_box) <- "+proj=longlat +datum=WGS84 +no_defs"
canada = crop(canada, clip_box)

# Read data file
results = read.csv("../summary_results.csv")
results = results[results$ID >= 15, ]

# Merge
strip_replace = function(str)
{
    str = stri_trans_general(str, 'Latin-ASCII')
    str = gsub("--", "-", str)
    if(str=="Mont-Royal (Mount Royal)") { str="Mont-Royal (Mount Royal)" }
    return(str)
}

# Strip accents and match up names
canada@data$ENNAME = sapply(canada@data$ENNAME, strip_replace)

# Merge data
merged_data <- merge(canada, results, by.x="ENNAME", by.y="Area")

# Make choropleth
pal = colorFactor(c("#e41a1c", "#377eb8"), merged_data$WinLastRound)
map = leaflet(merged_data) %>% addProviderTiles("CartoDB.Positron") %>% addPolygons(color = "#666666", fillColor = ~pal(WinLastRound), weight=1, opacity=1, fillOpacity=0.8) %>% setView(lng=-97, lat=58, zoom=4) %>% addLegend(colors=c("#e41a1c", "#377eb8"), labels=c("Bernier", "Scheer"))
#plot(map)

# Output map as PNG.
mapshot(map, file = "map.png")
