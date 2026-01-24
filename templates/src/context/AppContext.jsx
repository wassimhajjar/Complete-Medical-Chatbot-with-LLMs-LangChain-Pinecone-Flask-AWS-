import { createContext, useContext, useEffect, useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

const AppContext = createContext();
export const AppContextProvider = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [token, setToken] = useState(localStorage.getItem("token") || null);

  const backendUrl = import.meta.env.VITE_SERVER_URL;
  axios.defaults.baseURL = backendUrl;

  const fetchUser = async () => {
    try {
      console.log("abc");
      const { data } = await axios.get("/protected", {
        headers: { Authorization: token },
      });
      if (data) {
        setUser(data.user);
      } else {
        toast.error(data);
      }
    } catch (error) {
      toast.error(error);
    }
  };

  const createNewMessage = async () => {
    try {
      if (!user) {
        return toast("Login to create a new message");
      }
      navigate("/");
      const { data } = await axios.get("/messages", {
        headers: { Authorization: "Bearer " + token },
      });
      console.log("data", data);
      await fetchUserMessages();
    } catch (error) {
      toast.error(error.message);
    }
  };

  const fetchUserMessages = async () => {
    try {
      const { data } = await axios.get(`/messages/${user.id}`, {
        headers: { Authorization: token },
      });
      console.log("data2", data);
      if (data) {
        setMessages(data);
      }
    } catch (error) {
      toast.error(`error ${error}`);
    }
  };

  useEffect(() => {
    if (user) {
      fetchUserMessages();
    }
  }, [user]);

  useEffect(() => {
    if (token) {
      fetchUser();
    } else {
      setUser(null);
    }
  }, [token]);

  const value = {
    navigate,
    user,
    fetchUser,
    setUser,
    messages,
    setMessages,
    createNewMessage,
    fetchUserMessages,
    token,
    setToken,
    axios,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useAppContext = () => useContext(AppContext);
