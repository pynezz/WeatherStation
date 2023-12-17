// import { createSignal, onMount } from 'solid-js';

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

const WeatherWidget = (props) => {
    const reversedData = [...props.weatherData].reverse();

  return (
    <div class="max-w-2xl mx-auto p-4 bg-neutral-300 rounded-sm shadow-md">
      <h1 class="text-2xl font-semibold text-gray-800 mb-4">Weather Data</h1>
      <ul class="space-y-3">
        {reversedData.map((record) => (
          <li class="bg-slate-900 p-3 rounded-md">
           <p class="font-medium text-lg">Temperature: <span class="font-normal">{parseFloat(record.temperature).toFixed(2)}°C</span></p>
            <p class="font-medium text-lg">Humidity: <span class="font-normal">{parseFloat(record.humidity).toFixed(2)}%</span></p>            <p class="font-medium text-lg">
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
