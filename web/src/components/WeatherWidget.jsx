import { createSignal, onMount, onCleanup, createMemo } from 'solid-js';

const WeatherWidget = () => {
    const [latestData, setLatestData] = createSignal(null);
    const [historicalData, setHistoricalData] = createSignal([]);

    const handleWebSocketMessage = (event) => {
        const newData = JSON.parse(event.data);
        setLatestData(newData);
        setHistoricalData((prevData) => [...prevData, newData]);
    };

    onMount(() => {
      const socket = new WebSocket('ws://localhost:5000/ws');
      socket.onopen = function() {
          console.log('Websocket connection established!');
      };
      socket.onmessage = handleWebSocketMessage;

      onCleanup(() => {
          console.log("Close connection")
          socket.close();
      });
    });

    const currentTemp = createMemo(() => latestData() ? parseFloat(latestData().temperature).toFixed(2) : 'Loading...');
    const currentHum = createMemo(() => latestData() ? parseFloat(latestData().humidity).toFixed(2) : 'Loading...');


    return (
      <div>
        <div class="max-w-2xl mx-auto p-4 bg-neutral-300 rounded-sm shadow-md my-1">
          <h1 class="text-2xl font-semibold text-gray-800 mb-4">Weather now</h1>
          {latestData() && (
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="relative pb-[100%] mb-4 bg-zinc-700 rounded-md border">
                <div class="absolute top-0 left-0 right-0 bottom-0 flex flex-col items-center justify-center">
                  <p class={`text-3xl text-center font-mono ${currentTemp() !== 'Loading...' && parseFloat(currentTemp()) > 0 ? 'text-red-500' : 'text-blue-500'}`}>
                    {currentTemp()}°C
                  </p>
                  <p class="text-center text-sm font-bold mt-2">Temperature</p>
                </div>
              </div>
              <div class="relative pb-[100%] mb-4 bg-zinc-700 rounded-md border">
                <div class="absolute top-0 left-0 right-0 bottom-0 flex flex-col items-center justify-center">
                  <p class="text-3xl text-center font-mono">{currentHum}%</p>
                  <p class="text-center text-sm font-bold mt-2">Humidity</p>
                </div>
              </div>
            </div>
          )}
        </div>

        <div class="max-w-2xl mx-auto p-4 bg-neutral-300 rounded-sm shadow-md my-1">
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">Historical data</h2>
          <ul class="space-y-0.5">
            {historicalData().map((record, index) => (
              <li key={index} class="bg-zinc-600 p-3 rounded-md">
{/*
          TODO:
              Add time data:
                - minutes
                - hours
                - day
              And
                - season
*/}
                [{record.time}] Temp: {parseFloat(record.temperature).toFixed(2)} | Humidity: {parseFloat(record.humidity).toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
      </div>
    );


    return (
        <div class="max-w-2xl mx-auto p-4 bg-neutral-300 rounded-sm shadow-md">
            <h1 class="text-2xl font-semibold text-gray-800 mb-4">Weather Data</h1>
            <ul class="space-y-3">
                {weatherData().map((record) => (
                    <li class="bg-slate-900 p-3 rounded-md">
                        <p class="font-medium text-lg">Temperature: <span class="font-normal">{parseFloat(record.temperature).toFixed(2)}°C</span></p>
                        <p class="font-medium text-lg">Humidity: <span class="font-normal">{parseFloat(record.humidity).toFixed(2)}%</span></p>
                        <p class="font-medium text-lg">
                            Date: <span class="font-normal">{record.time.month}/{record.time.day}</span><br/>
                            Time: <span class="font-normal">{record.time.hour}:{record.time.minute}</span>
                        </p>
                        <p class="font-medium text-lg">Season: <span class="font-normal capitalize"/>{record.season}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default WeatherWidget;


// const WeatherWidget = () => {
//   const [weatherData, setWeatherData] = createSignal([]);

//   // Function to fetch weather data
//   async function fetchWeatherData() {
//     try {
//       const response = await fetch('http://localhost:5000/weather');
//       if (response.ok) {
//         const data = await response.json();
//         setWeatherData(data.data);
//       }
//     } catch (error) {
//       console.error('Error fetching weather data:', error);
//     }
//   }

//   // Fetch data on mount and set up a timer for regular updates
//   onMount(() => {
//     fetchWeatherData();
//     const interval = setInterval(fetchWeatherData, 6000); // Update every minute
//     return () => clearInterval(interval); // Cleanup on unmount
//   });

//   return (
//     <div>
//       <h1>Weather Data</h1>
//       <ul>
//         {weatherData().map((record) => (
//           <li>
//             <p>Temperature: {record.temperature}°C</p>
//             <p>Humidity: {record.humidity}%</p>
//             <p>Date: {record.time.month}/{record.time.day} Time: {record.time.hour}:{record.time.minute}</p>
//             <p>Season: {record.season}</p>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default WeatherWidget;


// const WeatherWidget = (props) => {
//   return (
//     <div>
//       <h1>Weather Data</h1>
//       <ul>
//         {props.weatherData.map((record) => (
//           <li>
//             <p>Temperature: {record.temperature}°C</p>
//             <p>Humidity: {record.humidity}%</p>
//             <p>Date: {record.time.month}/{record.time.day} Time: {record.time.hour}:{record.time.minute}</p>
//             <p>Season: {record.season}</p>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// };

// export default WeatherWidget;
