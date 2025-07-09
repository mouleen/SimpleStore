export const initialStore=()=>{
  return{
    message: null,
    token: localStorage.getItem('token') || null,
    user: localStorage.getItem('user') || null,
  }
}

export default function storeReducer(store, action = {}) {
  switch(action.type){
    case 'get_hello':
      return {
        ...store,
        message: action.payload
      };
    case 'get_token':
      return {
        ...store,
        token: action.payload
      };
    case 'get_user':
      return {
        ...store,
        user: action.payload
      };

    default:
      throw Error('Unknown action.');
  }    
}
