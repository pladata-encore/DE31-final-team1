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
  // get cookie
  const cookies = document.cookie.split(";").reduce((acc, cookie) => {
    const [key, value] = cookie.split("=").map(part => part.trim());
    acc[key] = value;
    return acc;
  }, {});
  // ref for modal
  const modalRef = React.useRef(null);
  const [radioValue, setRadioValue] = React.useState("");
  const [randomID, setRandomID] = React.useState(makeRandomID());
  const [name, setName] = React.useState("");
  const [dsList, setDsList] = React.useState([]);
  const [selectedDs, setSelectedDs] = React.useState([]);
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
    getdslist();
  }, []);

  function getdslist() {
    axios.get("http://192.168.1.230:19020/v1/data-source/getdslist", {
      params: {
        email: cookies.userEmail,
        token: cookies.userAuth,
      },
    }).then((res) => {
      console.log(res);
      setDsList(res.data);
    }).catch((err) => {
      console.log(err);
    });
  }

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
    const url = "http://192.168.1.230:19020/v1/data-group/createdg";
    let data = {
      email: cookies.userEmail,
      token: cookies.userAuth,
      id: randomID,
      type: radioValue,
    };
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

  function handleMultiSelect(e) {
    // if already selected, remove from selected list
    if (selectedDs.includes(e.target.value)) { 
      setSelectedDs(selectedDs.filter((el) => el !== e.target.value));
    } else {
      setSelectedDs(selectedDs.concat(e.target.value));
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
          Add Data Group
        </Typography>
        <div className='flex flex-row gap-4'>
        <ul className="flex flex-col gap-4">
          <li>
            <p>ID(Auto Generated)</p><Input label="Data Group ID" className='disabled:opacity-50' disabled id='id' value={randomID} />
          </li>
          <li>
            <p>Name(Optional)</p><Input label="Data Group Name" id='name' value={name} onChange={(e) => setName(e.target.value)} />
          </li>
          {/* scroll list to select data source(multiple at once) */}
          <li>
            <p>Data Source</p>
            {/* <select multiple className="w-full h-32 border border-blue-gray-200 rounded-lg p-2">
              {dsList.map((el) => (
                <option value={el.id}>{el.name}</option>
              ))}
            </select> */}
            <select multiple className="w-full h-32 border border-blue-gray-200 rounded-lg p-2" onChange={(e) => handleMultiSelect(e)} value={selectedDs}>
              <option value="ds1">Data Source 1</option>
              <option value="ds2">Data Source 2</option>
              <option value="ds3">Data Source 3</option>
              <option value="ds4">Data Source 4</option>
            </select>
          </li>
        </ul>
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