import { useContext } from "react";
//import { GlobalContext } from "../context/GlobalContext";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

export function useGlobalHelpers() {
  const {store,dispatch} =useGlobalReducer();  

  function logoutUser() {
      localStorage.removeItem("user");
      localStorage.removeItem("token");
      localStorage.removeItem("message");
      dispatch({type:"token", payload:"" });
      dispatch({type:"message", payload:"" });
      dispatch({type:"user", payload:"" });
  }

  function isLoggedIn() {
    return !!store.user;
  }
  function mockCafeterias() {
     return [
          {
              id: 1,
              name: "Brew & Co",
              image: "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=400",
              rating: 4.8,
              location: "Providencia, Santiago"
            },
            {
                id: 2,
                name: "Coffee Culture",
                image: "https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=400",
                rating: 4.7,
                location: "Ñuñoa, Santiago"
            },
            {
                id: 3,
                name: "The Bean House",
                image: "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400",
                rating: 4.6,
                location: "La Reina, Santiago"
            },
            {
                id: 4,
                name: "Café Aroma",
                image: "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=400",
                rating: 4.5,
                location: "Centro, Santiago"
            },
            {
                id: 5,
                name: "Verde Café",
                image: "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/18/d7/25/5b/20190818-130608-largejpg.jpg?w=1000&h=-1&s=1",
                rating: 4.3,
                location: "Las Condes, Santiago"
            },
            {
                id: 6,
                name: "Café Ritual",
                image: "https://images.unsplash.com/photo-1521017432531-fbd92d768814?w=400",
                rating: 4.2,
                location: "Vitacura, Santiago"
            }
        ];
    } 

  return { store, dispatch, logoutUser, isLoggedIn, mockCafeterias };
}
