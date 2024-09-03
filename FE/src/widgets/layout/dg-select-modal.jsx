import React from 'react';
import {
  Typography,
  Button,
  Card,
  CardHeader,
  Input,
} from "@material-tailwind/react";
import axios from 'axios';

export function DgSelModal() {
  // ref for modal
  const modalRef = React.useRef(null);
  const [radioValue, setRadioValue] = React.useState("");
  const [randomID, setRandomID] = React.useState(makeRandomID());
  const [name, setName] = React.useState("");
  const [databaseInfo, setDatabaseInfo] = React.useState({
    type: "default",
    host: "",
    user: "",
    password: "",
    database: "",
    table: "",
  });

  function makeRandomID() {
    // make random ID based on current time
    const time = new Date();
    const randID = Math.random(time.getTime()).toString(36).substr(2, 9);
    return randID;
  }

  // when modal's hidden class is toggled, reset input fields and make random ID
  React.useEffect(() => {
    if (!modalRef.current.classList.contains("hidden")) {
      setName("");
      setRandomID(makeRandomID());
    }
  }, []);

  function dataPopupClose() {
    document.getElementById("dataPopup").classList.toggle("hidden");
    setName("");
    setRandomID(makeRandomID());
    setRadioValue("type1");
    setDatabaseInfo({
      type: "default",
      host: "",
      user: "",
      password: "",
      database: "",
      table: "",
    });
  }

  function onPressSubmit() {
    // get type of radio button
    const type = radioValue;

    // use switch case to get data based on type
    let data = {};
    switch (type) {
      case "type1":
        doApiCall();
        break;
      case "type2":
        doApiCall();
        break;
    }
  }

  function doApiCall() {
    const url = "http://localhost:5000/api/data";
    const data = {};
    // make api call to get data
    const res = axios.post(url, data);
    // if success, close modal
    if (res.status === 200) {
      dataPopupClose();
    }

    // if error, show error message
    if (res.status !== 200) {
      alert("Error: " + res.data);
    }

  }

  return (
    // make data popup covering full page
    <div className="absolute top-0 left-0 w-full h-full hidden z-50" id="dataPopup" ref={modalRef}>
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-8 rounded-xl border border-blue-gray-200">
        {/* close button */}
        <button className="absolute top-2 right-2" onClick={() => dataPopupClose()}>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
        <Typography variant="h6" color="white">
          Add Data Source
        </Typography>
        {/* radio button to select type */}
        <div className="flex items-stretch items-center justify-center mb-4">
          {/* radio button check state base on radioValue */}
          <input type="radio" id="type1" name="type" value="type1" className="mr-2" onChange={(e) => setRadioValue(e.target.value)} />
          <label htmlFor="type1">Streaming</label>
          <input type="radio" id="type2" name="type" value="type2" className="ml-4 mr-2" onChange={(e) => setRadioValue(e.target.value)}/>
          <label htmlFor="type2">Database</label>
        </div>
        <div className='flex flex-row gap-4'>
        <ul className="flex flex-col gap-4">
          <li>
            <p>ID(Auto Generated)</p><Input label="Data Source Name" className='disabled:opacity-50' disabled id='id' value={randomID} />
          </li>
          <li>
            <p>Name(Optional)</p><Input label="Data Source Name" id='name' value={name} onChange={(e) => setName(e.target.value)} />
          </li>
          {/* if radio value */}
          {radioValue === "type2" && (
            <li>
              {/* make dropdown selector */}
              <p>Database</p>
              <select className="w-full border border-blue-gray-200 rounded-lg p-2" value={databaseInfo.type} onChange={(e) => setDatabaseInfo({...databaseInfo, type: e.target.value})}>
                <option value="default">Select Database</option>
                <option value="mysql">MySQL</option>
                <option value="postgresql">PostgreSQL</option>
              </select>
            </li>
          )}
        </ul>
        {/* if database type is not default */}
        {(databaseInfo.type !== "default" && radioValue === "type2") && (
          <ul className="flex flex-col gap-4">
            <li>
              <p>Host</p><Input id='host' value={databaseInfo.host} onChange={(e) => setDatabaseInfo({...databaseInfo, host: e.target.value})} placeholder="127.0.0.1:3306" />
            </li>
            <li>
              <p>User</p><Input label="User" id='user' value={databaseInfo.user} onChange={(e) => setDatabaseInfo({...databaseInfo, user: e.target.value})} />
            </li>
            <li>
              <p>Password</p><Input label="Password" id='password' value={databaseInfo.password} onChange={(e) => setDatabaseInfo({...databaseInfo, password: e.target.value})} />
            </li>
            <li>
              <p>Database</p><Input label="Database" id='database' value={databaseInfo.database} onChange={(e) => setDatabaseInfo({...databaseInfo, database: e.target.value})} />
            </li>
            <li>
              <p>Table</p><Input label="Table" id='table' value={databaseInfo.table} onChange={(e) => setDatabaseInfo({...databaseInfo, table: e.target.value})} />
            </li>
          </ul>
        )}
        </div>

        {/* button for submit, align center */}
        <Button color="blue" onClick={() => onPressSubmit()} className="mt-4 w-full">
          Submit
        </Button>
      </div>
    </div>
  );
}

export default DgSelModal;