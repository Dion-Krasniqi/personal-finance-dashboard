import { useState } from 'react'

export default function Register() {

    const [formData, setFormData] = useState({'email':'',
                                              'passowrd1':'',
                                              'password2':''
                                            });
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]:e.target.value
        })

    }

  return (
    <div>
        <h2>Register</h2>
        <form>
            <label>Email:</label><br/>
            <input type='email' name='email' value={formData.email} onChange={handleChange}></input><br/>
            <label>Password:</label><br/>
            <input type='password' name='password1' value={formData.password1} onChange={handleChange}></input><br/>
            <label>Confirm Password:</label><br/>
            <input type='password' name='password2' value={formData.password2} onChange={handleChange}></input><br/>

        </form>
    </div>
  )
}

