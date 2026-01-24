import React from "react";
import { Route, Routes } from "react-router-dom";
import ChatBox from "./pages/ChatBox";
import { useAppContext } from "./context/AppContext";
import Login from "./pages/Login";
import { Toaster } from "react-hot-toast";

const App = () => {
  const { user } = useAppContext();
  // console.log("user", user);
  return (
    <>
      <Toaster />
      {user ? (
        <>
          <div className="dark:bg-linear-to-b from-[#242124] to-[#000000] dark:text-white">
            <div className="h-screen">
              <Routes>
                <Route path="/" element={<ChatBox />} />
              </Routes>
            </div>
          </div>
        </>
      ) : (
        <div className="bg-linear-to-b from-[#242124] to-[#000000] flex items-center justify-center h-screen w-screen">
          <Login />
        </div>
      )}
    </>
  );
};

export default App;
