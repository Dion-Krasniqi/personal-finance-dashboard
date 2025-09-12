import { useState, useEffect } from "react"
import axios from 'axios';


export default function Home () {

  const [email, setEmail] = useState('');
  const [isLoggedIn, setisLoggedIn] = useState(false);

  useEffect( ()=>{
    const checkLoggedIn = async () =>{
      try {
        const token = localStorage.getItem('accessToken')
        if (token){
    
          const config = { headers: {'Authorization':`Bearer ${token}`}};
          const response = await axios.get('http://192.168.1.9:8000/accounts/user/', config)
          setisLoggedIn(true);
          setEmail(response.data.email);
        } else {
          setisLoggedIn(false);
          setEmail('');
        }
      }catch {
        setisLoggedIn(false);
        setEmail('');
    }};
     checkLoggedIn()}, [])

     const handleLogout = async () => {
        try {
          const refreshToken = localStorage.getItem('refreshToken');
          const token = localStorage.getItem('accessToken');
          const config = { headers: {'Authorization':`Bearer ${token}`}};
          if (refreshToken) {
            await axios.post('http://192.168.1.9:8000/accounts/logout/',{'refresh': refreshToken}, config);
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            setisLoggedIn(false);
            setEmail('');
          }

        } catch(error) {
          console.log('Failed to log out')
        }
     }

  
  return (
    <div>
      {isLoggedIn ? (<div>Hi, {email}</div>):('Please log in')}
      <button onClick={handleLogout}></button>
    </div>
    
  )
}
