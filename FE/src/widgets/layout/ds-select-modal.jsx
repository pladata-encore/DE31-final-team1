import React from 'react';
import {
  Typography,
  Button,
  Card,
  CardHeader,
  Input,
} from "@material-tailwind/react";

export function DsSelModal() {
  // ref for modal
  const modalRef = React.useRef(null);
  const [randomID, setRandomID] = React.useState(makeRandomID());
  const [name, setName] = React.useState("");

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
  }


  return (
    // make data popup covering full page
    <div className="absolute top-0 left-0 w-full h-full hidden z-50" id="dataPopup" ref={modalRef}>
      <div className="absolute top-2/3 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-8 rounded-xl border border-blue-gray-200">
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
          <input type="radio" id="type1" name="type" value="type1" className="mr-2"/>
          <label htmlFor="type1">Type 1</label>
          <input type="radio" id="type2" name="type" value="type2" className="ml-4 mr-2"/>
          <label htmlFor="type2">Type 2</label>
        </div>
        <ul className="flex flex-col gap-4">
          <li>
            <p>ID(Auto Generated)</p><Input label="Data Source Name" className='disabled:opacity-50' disabled id='id' value={randomID} />
          </li>
          <li>
            <p>Name(Optional)</p><Input label="Data Source Name" id='name' value={name} onChange={(e) => setName(e.target.value)} />
          </li>
        </ul>
      </div>
    </div>
  );
}

export default DsSelModal;