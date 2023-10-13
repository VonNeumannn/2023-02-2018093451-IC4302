import React, { useState, useEffect } from "react";
import userImage from '../assets/user.png'
import Eye from '../assets/show-password-eye.png';
import NotEye from '../assets/hide-password-eye.png';
import { Link, useNavigate } from "react-router-dom";
import axios from 'axios';
import ModalError from "./ModalError";
import ModalInfo from "./ModalInfo";

export default function Login() {
    document.title = "Inicio de sesión"
    const [stateButtom, changeState] = useState(false);
    const navigate = useNavigate();
    const swapPassword = () => {
        changeState(!stateButtom);
    };

    const handleAccess = () => {
        const modal = document.getElementById("modal-container")
        const modalInfo = document.getElementById("modal-info")
        const email = document.getElementById('email-text').value;
        const password = document.getElementById('password-input').value;
        var mensajeError = document.getElementById("mensaje-error");
        var mensajeError2 = document.getElementById("mensaje-error2");
        mensajeError.textContent = "";

        mensajeError2.textContent = "";
        
        modalInfo.classList.remove('ocultando')
        modalInfo.classList.add('mostrando')
        if (modal.classList.value.includes("mostrando") ) {

            modal.classList.remove('mostrando');
            modal.classList.add('ocultando');
            
        }
        
        if (email.trim() != "" && password.trim() != "") {

            const apiUrl = 'http://172.17.0.2:5000/login';

            // Datos que deseas enviar en la solicitud POST
            const data = {
                "email": email,
                "password": password
            };


            // Realizar la solicitud POST
            axios.post(apiUrl, data)
                .then(response => {
                    if (response.data.status) {
                        navigate('/search')
                    } else {
                        alert(response.data.message)
                    }
                })
                .catch(error => {
                    // Si ocurre un error en la solicitud
                    //console.error('Error en la solicitud:', error);
                    //console.error('Error en la solicitud:', error);
                    //console.error('Error en la solicitud:', error);
                    try {
                        alert(JSON.parse(error.request.response).message)
                    } catch (error) {
                        modalInfo.classList.remove('mostrando')
                        modalInfo.classList.add('ocultando')
                        modal.classList.remove('ocultando');
                        modal.classList.add('mostrando');
                    }
                });


        } else {
            if (email.trim() === "") {
                mensajeError.textContent = "El campo 'Correo' es necesario";

            }

            if (password.trim() === "") {
                mensajeError2.textContent = "El campo 'Contraseña' es necesario";

            }
        }
    }





    return (
        <div className="login-screen-view-new">
            <ModalError/>
            <ModalInfo text={"Buscando su usuario en la base de dato. Espere un momento."}/>
            <div className="login-frame">

                <img src={userImage} alt="usuarioImagen" />
                <h1>Login WikiSearch</h1>


                <input type="text" id="email-text" placeholder="Ingrese su correo" autoFocus />
                <p id="mensaje-error" className="mensaje-error"></p>

                <div className="password-space">


                    <input type={stateButtom ? "text" : "password"} id="password-input" placeholder="Ingrese su contraseña" required />
                    <button id="eye-button" type="button" onClick={swapPassword}>
                        <img src={stateButtom ? NotEye : Eye} id="eye-image" alt="Set password visible or not" />
                    </button>

                </div>
                <p id="mensaje-error2" className="mensaje-error"></p>


                <button className="submit-login" onClick={handleAccess}>
                    Ingresar
                </button>

                <p className="create-account">¿No tenés una cuenta?
                    <Link to="/register"> Registrate aquí</Link></p>
            </div>
        </div>

    );
}