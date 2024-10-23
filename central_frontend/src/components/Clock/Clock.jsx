import { useState, useEffect } from "react";

const months = [
  "Styczeń",
  "Luty",
  "Marzec",
  "Kwiecień",
  "Maj",
  "Czerwiec",
  "Lipiec",
  "Sierpień",
  "Wrzesień",
  "Październik",
  "Listopad",
  "Grudzień",
];

export default function Clock() {
  var [date, setDate] = useState(new Date());

  useEffect(() => {
    var timer = setInterval(() => setDate(new Date()), 1000);
    return function cleanup() {
      clearInterval(timer);
    };
  });

  return (
    <div id="clock">
      <h1>{date.toLocaleTimeString("pl-PL")}</h1>
      <h3>
        {date.getDate()} {months[date.getMonth()]} {date.getFullYear()}
      </h3>
    </div>
  );
}
