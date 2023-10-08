import React, { useState, useEffect } from "react";
import userImage from '../assets/user.png'
import Eye from '../assets/show-password-eye.png';
import NotEye from '../assets/hide-password-eye.png';
import { Link, useNavigate } from "react-router-dom";

export default function Login() {

    const [stateButtom, changeState] = useState(false);
    const navigate = useNavigate();
    const swapPassword = () => {
        changeState(!stateButtom);
    };

    const handleAccess = () => {
        const email = document.getElementById('email-text').value;
        const password = document.getElementById('password-input').value;
        console.log(email+" + "+password)

        fetch('https://hmnlr3nl-5000.use2.devtunnels.ms/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "email": email, "password": password
            }),
        }).then((res) => res.json())
            .then((data) => {

                if (data.status) {
                    navigate('/search')


                } else {
                    alert(data.message)
                }

            })


            .catch(error => {
                console.log('Error al obtener datos desde el backend:', error);
            })
    }

    

document.title = "Inicio de sesión"

return (
    <div className="login-screen-view">
        <div className="login-frame">
            <img src={userImage} alt="usuarioImagen" />
            <h1>Login WikiSearch</h1>

            <input type="text" id="email-text" placeholder="Ingrese su correo" autoFocus />

            <div className="password-space">

                <input type={stateButtom ? "text" : "password"} id="password-input" placeholder="Ingrese su contraseña" required />
                <button id="eye-button" type="button" onClick={swapPassword}>
                    <img src={stateButtom ? NotEye : Eye} id="eye-image" alt="Set password visible or not" />
                </button>
            </div>

            <button className="submit-login" onClick={handleAccess}>
                Ingresar
            </button>
            <p className="create-account">¿No tenés una cuenta?
                <Link to="/register"> Registrate aquí</Link></p>
        </div>
    </div>

);
}