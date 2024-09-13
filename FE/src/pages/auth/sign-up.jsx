import {
  Card,
  Input,
  Checkbox,
  Button,
  Typography,
} from "@material-tailwind/react";
import { Link, useNavigate } from "react-router-dom";
import React from "react";
import axios from "axios";

// axios custom header for evade cors error
axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";
axios.defaults.headers.post["Access-Control-Allow-Headers"] = "*";
axios.defaults.headers.post["Access-Control-Allow-Methods"] = "*";
axios.defaults.headers.post["Content-Type"] = "application/json";


export function SignUp() {
  const navigate = useNavigate();
  const [regForm, setRegForm] = React.useState({
    email: "",
    name: "",
    password: "",
    isCheck: false,
  });

  function checkFormValidation() {
    // check form validation
    if(regForm.email === "" || regForm.name === "" || regForm.password === ""){
      return "ERR_EMPTY";
    } else if(regForm.isCheck === false){
      return "ERR_CHECK";
    } else if(RegExp("^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$").test(regForm.email) === false){
      return "ERR_EMAIL";
    } else if(RegExp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[!@#$%^&*()_+\\[\\]{}|;:\'",.<>/?`~\\-])[a-zA-Z0-9!@#$%^&*()_+\\[\\]{}|;:\'",.<>/?`~\\-]{8,16}$').test(regForm.password) === false){
      return "ERR_PASSWORD";
    }
    return "OK";
  }

  function onClickRegister() {
    console.log("Register");
    // check form validation
    const formValidation = checkFormValidation();
    if(formValidation !== "OK"){
      console.log("Form validation error", formValidation);
      // show error modal
      // show modal
      // setIsError(true);
      return;
    }

    // make object to send to api
    const regUserInfo = {
      email: regForm.email,
      name: regForm.name,
      password: btoa(regForm.password) // encode password to base64
    }

    console.log(regUserInfo);
    // call register api
    axios.post("http://192.168.1.230:19020/v1/users/createUser/", regUserInfo)
    .then((res) => {
      // if res status is 200, save user info to cookie and redirect to main page
      if(res.status === 200 || res.status === 201){
        document.cookie = `userEmail=${res.data.email}; expires=${new Date(Date.now() + 3600 * 1000).toUTCString()}; path=/`; 
        document.cookie = `userName=${res.data.name}; expires=${new Date(Date.now() + 3600 * 1000).toUTCString()}; path=/`;
        document.cookie = `userAuth=${res.data.access_token}; expires=${new Date(Date.now() + 3600 * 1000).toUTCString()}; path=/`;
        navigate("/dashboard/home");
      } else if(res.status === 409){
        alert("Email already exists");
      } else {
        console.log("Register error");
      }
    });
  }

  return (
    <section className="m-8 flex">
            <div className="w-2/5 h-full hidden lg:block">
        <img
          src="/img/pattern.png"
          className="h-full w-full object-cover rounded-3xl"
        />
      </div>
      <div className="w-full lg:w-3/5 flex flex-col items-center justify-center">
        <div className="text-center">
          <Typography variant="h2" className="font-bold mb-4">Join Us Today</Typography>
          <Typography variant="paragraph" color="blue-gray" className="text-lg font-normal">Enter your email and password to register.</Typography>
        </div>
        <form className="mt-8 mb-2 mx-auto w-80 max-w-screen-lg lg:w-1/2">
          <div className="mb-1 flex flex-col gap-6">
            <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
              Your email
            </Typography>
            <Input
              size="lg"
              placeholder="name@mail.com"
              className=" !border-t-blue-gray-200 focus:!border-t-gray-900"
              labelProps={{
                className: "before:content-none after:content-none",
              }}
              onChange={(e) => setRegForm({ ...regForm, email: e.target.value })}
            />
            <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
              Your name
            </Typography>
            <Input
              size="lg"
              placeholder="John Doe"
              className=" !border-t-blue-gray-200 focus:!border-t-gray-900"
              labelProps={{
                className: "before:content-none after:content-none",
              }}
              onChange={(e) => setRegForm({ ...regForm, name: e.target.value })}
            />
            <Typography variant="small" color="blue-gray" className="-mb-3 font-medium">
              Password
            </Typography>
            <Input
              size="lg"
              placeholder="********"
              type="password"
              className=" !border-t-blue-gray-200 focus:!border-t-gray-900"
              labelProps={{
                className: "before:content-none after:content-none",
              }}
              onChange={(e) => setRegForm({ ...regForm, password: e.target.value })}
            />
          </div>
          <Checkbox
            label={
              <Typography
                variant="small"
                color="gray"
                className="flex items-center justify-start font-medium"
              >
                I agree the&nbsp;
                <a
                  href="#"
                  className="font-normal text-black transition-colors hover:text-gray-900 underline"
                >
                  Terms and Conditions
                </a>
              </Typography>
            }
            containerProps={{ className: "-ml-2.5" }}
            onChange={(e) => setRegForm({ ...regForm, isCheck: e.target.checked })}
          />
          <Button
          className="mt-6" fullWidth
          onClick={onClickRegister}
          >
            Register Now
          </Button>
          <Typography variant="paragraph" className="text-center text-blue-gray-500 font-medium mt-4">
            Already have an account?
            <Link to="/auth/sign-in" className="text-gray-900 ml-1">Sign in</Link>
          </Typography>
        </form>

      </div>
    </section>
  );
}

export default SignUp;
