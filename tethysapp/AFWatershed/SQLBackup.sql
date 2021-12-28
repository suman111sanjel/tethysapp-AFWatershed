
UPDATE
   public.watershed_layergrouptwo
SET
   wms_url = REPLACE(wms_url,'http://192.168.11.242:8082/thredds/wms/watershed/','http://192.168.11.242:8081/thredds/wms/watershed_data/')



UPDATE
   public.watershed_layergrouptwo
SET
   wms_url = REPLACE(wms_url,'http://192.168.11.242:8082/thredds/catalog/watershed/','http://192.168.11.242:8081/thredds/catalog/watershed_data/')


UPDATE
   public.watershed_layergrouptwo
SET
   wms_url = REPLACE(wms_url,'http://192.168.11.242:8081/thredds/','http://110.34.30.197:8080/thredds/')


UPDATE public.watershed_layergrouptwo
	SET legend=REPLACE(legend,'http://192.168.11.242:8081/thredds/','http://110.34.30.197:8080/thredds/');


UPDATE
   public.watershed_layergrouptwo
SET
   wms_url = REPLACE(wms_url,'http://192.168.11.242:8081/thredds/catalog/watershed_data/')



UPDATE
   public.watershed_layergrouptwo
SET
   sld_body_thredds = REPLACE(sld_body_thredds,'%23','#')


UPDATE
   public.watershed_layergrouptwo
SET
   wms_url = REPLACE(wms_url,'http://tethys.icimod.org:8080/geoserver/watershed/wms','http://110.34.30.197:8080/geoserver/AfghanistanWatershed/wms')

where server_type='geoserver';

UPDATE
   public.watershed_layergrouptwo
SET
   layernamegeoserver = REPLACE(layernamegeoserver,'watershed:','AfghanistanWatershed:')
where server_type='geoserver';
