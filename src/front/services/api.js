const backendUrl = import.meta.env.VITE_BACKEND_URL

export const getToken = async (form) => {
    const response = await fetch(backendUrl + "/api/login",  {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(form),
        });
    const jsonResponse = await response.json();
    return jsonResponse;
}


export const registerUser = async (form) => {
    const response = await fetch(backendUrl + "/api/register",  {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(form),
        });
    const jsonResponse = await response.json();
    return jsonResponse;
}
export const getHello = async (token) => {
    const response = await fetch(backendUrl + "/api/hello" ,  {
          method: "GET",
          headers: { "Content-Type": "application/json" , "Authorization":"Bearer " + token }
        });
    const jsonResponse = await response.json();
    return jsonResponse;
}