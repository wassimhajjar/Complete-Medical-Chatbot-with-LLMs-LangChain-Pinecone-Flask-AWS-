import React, { useState } from "react";
import { useAppContext } from "../context/AppContext";
import toast from "react-hot-toast";

const Login = () => {
  const { axios, setToken, navigate } = useAppContext();

  const [state, setState] = useState("login");

  const [name, setName] = useState("");

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const url = state === "login" ? "/login" : "/signup";
    console.log("data login0");

    try {
      const { data } = await axios.post(url, { name, email, password });
      console.log("token", `Bearer ${data.token}`);
      if (data) {
        if (state === "login") {
          setToken(`Bearer ${data.token}`);
          localStorage.setItem("token", `Bearer ${data.token}`);
          navigate("/");
        } else setState("login");
      }
    } catch (error) {
      toast.error(error.response.data.detail);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col gap-4 m-auto items-start p-8 py-12 w-80 sm:w-[352px] text-gray-500 rounded-lg shadow-xl border border-gray-200 bg-white"
    >
      <p className="text-2xl font-medium m-auto">
        <span className="text-purple-700">User</span>{" "}
        {state === "login" ? "Login" : "Sign Up"}
      </p>

      {state === "signup" && (
        <div className="w-full">
          <p>Name</p>

          <input
            onChange={(e) => setName(e.target.value)}
            value={name}
            placeholder="type here"
            className="border border-gray-200 rounded w-full p-2 mt-1 outline-purple-700"
            type="text"
            required
          />
        </div>
      )}

      <div className="w-full ">
        <p>Email</p>

        <input
          onChange={(e) => setEmail(e.target.value)}
          value={email}
          placeholder="type here"
          className="border border-gray-200 rounded w-full p-2 mt-1 outline-purple-700"
          type="email"
          required
        />
      </div>

      <div className="w-full ">
        <p>Password</p>

        <input
          onChange={(e) => setPassword(e.target.value)}
          value={password}
          placeholder="type here"
          className="border border-gray-200 rounded w-full p-2 mt-1 outline-purple-700"
          type="password"
          required
        />
      </div>

      {state === "signup" ? (
        <p>
          Already have account?{" "}
          <span
            onClick={() => setState("login")}
            className="text-purple-700 cursor-pointer"
          >
            click here
          </span>
        </p>
      ) : (
        <p>
          Create an account{" "}
          <span
            onClick={() => setState("signup")}
            className="text-purple-700 cursor-pointer"
          >
            click here
          </span>
        </p>
      )}

      <button
        type="submit"
        className="bg-purple-700 hover:bg-purple-800 transition-all text-white w-full py-2 rounded-md cursor-pointer"
      >
        {state === "signup" ? "Create Account" : "Login"}
      </button>
    </form>
  );
};
export default Login;
