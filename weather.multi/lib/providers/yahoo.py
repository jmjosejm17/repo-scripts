from ..conversions import *

class Weather():
    def __init__():
        pass

    def get_weather(response, loc, locid):
        data = response['weathers'][0]
    #current - standard
        set_property('Location'                  , loc)
        set_property('Updated'                   , convert_datetime(data['observation']['observationTime']['timestamp'], 'datetime', 'timedate', None))
        set_property('Current.Location'          , data['location']['displayName'])
        set_property('Current.Condition'         , data['observation']['conditionDescription'])
        set_property('Current.Temperature'       , convert_temp(data['observation']['temperature']['now'], 'F', 'C'))
        set_property('Current.UVIndex'           , str(data['observation']['uvIndex']))
        set_property('Current.OutlookIcon'       , '%s.png' % str(data['observation']['conditionCode'])) # Kodi translates it to Current.ConditionIcon
        set_property('Current.FanartCode'        , str(data['observation']['conditionCode']))
        set_property('Current.Wind'              , convert_speed(data['observation']['windSpeed'], 'mph', 'kmh'))
        set_property('Current.WindDirection'     , xbmc.getLocalizedString(WIND_DIR(data['observation']['windDirection'])))
        set_property('Current.Humidity'          , str(data['observation']['humidity']))
        set_property('Current.DewPoint'          , dewpoint(int(convert_temp(data['observation']['temperature']['now'], 'F', 'C')), data['observation']['humidity']))
        set_property('Current.FeelsLike'         , convert_temp(data['observation']['temperature']['feelsLike'], 'F', 'C'))
    #current - extended
        set_property('Current.WindChill'         , convert_temp(windchill(data['observation']['temperature']['now'], data['observation']['windSpeed']), 'F') + TEMPUNIT)
        if 'F' in TEMPUNIT:
            set_property('Current.Visibility'    , str(round(data['observation']['visibility'],2)) + ' mi')
            set_property('Current.Pressure'      , str(round(data['observation']['barometricPressure'],2)) + ' inHg')
        else:
            set_property('Current.Visibility'        , str(round(1.60934 * data['observation']['visibility'],2)) + ' km')
            set_property('Current.Pressure'      , str(int(round((33.864 * data['observation']['barometricPressure'])))) + ' mbar')
        set_property('Current.Precipitation'     , str(data['observation']['precipitationProbability']) + '%')
        set_property('Current.IsFetched'         , 'true')
    #forecast - extended
        set_property('Forecast.City'            , data['location']['displayName'])
        set_property('Forecast.Country'         , data['location']['countryName'])
        set_property('Forecast.Latitude'        , str(data['location']['latitude']))
        set_property('Forecast.Longitude'       , str(data['location']['longitude']))
        set_property('Forecast.Updated'         , convert_datetime(data['observation']['observationTime']['timestamp'], 'datetime', 'timedate', None))
        set_property('Forecast.IsFetched'       , 'true')
    #today - extended
        set_property('Today.Sunrise'             , convert_datetime(data['sunAndMoon']['sunrise'], 'seconds', 'time', None))
        set_property('Today.Sunset'              , convert_datetime(data['sunAndMoon']['sunset'], 'seconds', 'time', None))
        set_property('Today.Moonphase'           , MOONPHASE[data['sunAndMoon']['moonPhase']])
        set_property('Today.IsFetched'           , 'true')
    #hourly - extended
        for count, item in enumerate(data['forecasts']['hourly']):
            set_property('Hourly.%i.Time'            % (count + 1), convert_datetime(item['observationTime']['timestamp'], 'datetime', 'time', None))
            set_property('Hourly.%i.LongDate'        % (count + 1), convert_datetime(item['observationTime']['timestamp'], 'datetime', 'monthday', 'long'))
            set_property('Hourly.%i.ShortDate'       % (count + 1), convert_datetime(item['observationTime']['timestamp'], 'datetime', 'monthday', 'short'))
            set_property('Hourly.%i.Temperature'     % (count + 1), convert_temp(item['temperature']['now'], 'F') + TEMPUNIT)
            set_property('Hourly.%i.FeelsLike'       % (count + 1), convert_temp(item['temperature']['feelsLike'], 'F') + TEMPUNIT)
            set_property('Hourly.%i.Outlook'         % (count + 1), str(item['conditionDescription']))
            set_property('Hourly.%i.OutlookIcon'     % (count + 1), '%s.png' % str(item['conditionCode']))
            set_property('Hourly.%i.FanartCode'      % (count + 1), str(item['conditionCode']))
            set_property('Hourly.%i.Humidity'        % (count + 1), str(item['humidity']) + '%')
            set_property('Hourly.%i.Precipitation'   % (count + 1), str(item['precipitationProbability']) + '%')
            set_property('Hourly.%i.WindDirection'   % (count + 1), xbmc.getLocalizedString(WIND_DIR(item['windDirection'])))
            set_property('Hourly.%i.WindSpeed'       % (count + 1), convert_speed(item['windSpeed'], 'mph') + SPEEDUNIT)
            set_property('Hourly.%i.WindDegree'      % (count + 1), str(item['windDirection']) + u'°')
            set_property('Hourly.%i.DewPoint'        % (count + 1), convert_temp(dewpoint(int(convert_temp(item['temperature']['now'], 'F', 'C')), item['humidity']), 'C') + TEMPUNIT)
        set_property('Hourly.IsFetched'              , 'true')
