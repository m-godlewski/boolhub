import { putSettings } from "./Settings.jsx"



export default function SettingsForm(props) {

    // method that handle submit button click
    const handleSubmit = (e) => {
        e.preventDefault();
        putSettings(e.target)
            .then((result) => {
                alert(result);
            },
                (error) => {
                    alert(error);
                })
    };

    return (
        <div className="container">

            <form onSubmit={handleSubmit}>

                <section>
                    <label>Minimalna Temperatura</label>
                    <input type="text" name="temperature_min" required defaultValue={props.settings.temperature_min} placeholder="" />
                </section>
                <section>
                    <label>Maksymalna Temperatura</label>
                    <input type="text" name="temperature_max" required defaultValue={props.settings.temperature_max} placeholder="" />
                </section>
                <section>
                    <label>Powiadamiaj o Temperaturze</label>
                    <input type="text" name="notify_temperature" required defaultValue={props.settings.notify_temperature} placeholder="" />
                </section>

                <section>
                    <label>Minimalna Wilgotność Powietrza</label>
                    <input type="text" name="humidity_min" required defaultValue={props.settings.humidity_min} placeholder="" />
                </section>
                <section>
                    <label>Maksymalna Wilgotność Powietrza</label>
                    <input type="text" name="humidity_max" required defaultValue={props.settings.humidity_max} placeholder="" />
                </section>
                <section>
                    <label>Powiadamiaj o Wilgotności Powietrza</label>
                    <input type="text" name="notify_humidity" required defaultValue={props.settings.notify_humidity} placeholder="" />
                </section>

                <section>
                    <label>Próg Zanieczyszczenia Powietrza</label>
                    <input type="text" name="aqi_threshold" required defaultValue={props.settings.aqi_threshold} placeholder="" />
                </section>
                <section>
                    <label>Powiadamiaj o Zanieczyszczeniu Powietrza</label>
                    <input type="text" name="notify_aqi" required defaultValue={props.settings.notify_aqi} placeholder="" />
                </section>

                <section>
                    <label>Próg Obciążenia Sieci</label>
                    <input type="text" name="network_overload_threshold" required defaultValue={props.settings.network_overload_threshold} placeholder="" />
                </section>
                <section>
                    <label>Powiadamiaj o Obciążeniu Sieci</label>
                    <input type="text" name="notify_network_overload" required defaultValue={props.settings.notify_network_overload} placeholder="" />
                </section>
                <section>
                    <label>Powiadamiaj o Nieznanym Urządzeniu w Sieci</label>
                    <input type="text" name="notify_unknown_device" required defaultValue={props.settings.notify_unknown_device} placeholder="" />
                </section>

                <section>
                    <label>Poziom baterii/filtra</label>
                    <input type="text" name="health_threshold" required defaultValue={props.settings.health_threshold} placeholder="" />
                </section>
                <section>
                    <label>Powiadomienia Diagnostyczne</label>
                    <input type="text" name="notify_health" required defaultValue={props.settings.notify_health} placeholder="" />
                </section>

                <section>
                    <label>API systemu pogodowego</label>
                    <input type="text" name="weather_api_url" defaultValue={props.settings.weather_api_url} placeholder="" />
                </section>
                <section>
                    <label>Szerokość Geograficzna</label>
                    <input type="text" name="weather_api_latitude" defaultValue={props.settings.weather_api_latitude} placeholder="" />
                </section>
                <section>
                    <label>Długość Geograficzna</label>
                    <input type="text" name="weather_api_longitude" defaultValue={props.settings.weather_api_longitude} placeholder="" />
                </section>
                <section>
                    <label>API Token</label>
                    <input type="text" name="weather_api_token" defaultValue={props.settings.weather_api_token} placeholder="" />
                </section>

                <section>
                    <p></p>
                    <button variant="primary" type="submit">
                        Zapisz
                    </button>
                </section>
            </form>

        </div >
    );
};
