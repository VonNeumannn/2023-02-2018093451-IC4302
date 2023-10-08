import React, { useState, useEffect } from "react";
import userImage from '../assets/user.png'
import Eye from '../assets/show-password-eye.png';
import NotEye from '../assets/hide-password-eye.png';
import { Link, useNavigate } from "react-router-dom";

export default function Register() {
    
    const navigate = useNavigate()
    const handleAccess = () => {
             // Obtén una referencia al campo de entrada y al párrafo de mensaje de error
             var inputNombre = document.getElementById("name-text");
             var inputApellido = document.getElementById("last-name-text");
             var inputCorreo = document.getElementById("email-text");
             var inputContra = document.getElementById("password-text");
             var mensajeError = document.getElementById("mensaje-error");
             var mensajeError2 = document.getElementById("mensaje-error2");
             var mensajeError3 = document.getElementById("mensaje-error3");
             var mensajeError4 = document.getElementById("mensaje-error4");
     
             // Agrega un controlador de eventos para el evento 'input' (cada vez que se escriba algo en el campo)
             
                 var valor = inputNombre.value.trim();
     
                 // Realiza la validación, por ejemplo, si el campo no está vacío
                 if (valor === "") {
                     mensajeError.textContent = "El campo nombre es requerido.";
                 } else {
                     mensajeError.textContent = ""; // Limpia el mensaje de error si la validación pasa
                 }
       
    
                 var valor = inputApellido.value.trim();
     
                 // Realiza la validación, por ejemplo, si el campo no está vacío
                 if (valor === "") {
                     mensajeError2.textContent = "El campo nombre es requerido.";
                 } else {
                     mensajeError2.textContent = ""; // Limpia el mensaje de error si la validación pasa
                 }
             
             // Agrega un controlador de eventos para el evento 'input' (cada vez que se escriba algo en el campo)
          
                 var valor = inputCorreo.value.trim();
     
                 // Realiza la validación, por ejemplo, si el campo no está vacío
                 if (valor === "") {
                     mensajeError3.textContent = "El campo nombre es requerido.";
                 } else {
                     mensajeError3.textContent = ""; // Limpia el mensaje de error si la validación pasa
                 }
            
             // Agrega un controlador de eventos para el evento 'input' (cada vez que se escriba algo en el campo)

                 var valor = inputContra.value.trim();
     
                 // Realiza la validación, por ejemplo, si el campo no está vacío
                 if (valor === "") {
                     mensajeError4.textContent = "El campo nombre es requerido.";
                 } else {
                     mensajeError4.textContent = ""; // Limpia el mensaje de error si la validación pasa
                 }
             
        //navigate('/search');
    }
    useEffect(() => {
                     // Obtén una referencia al campo de entrada y al párrafo de mensaje de error
                     var inputNombre = document.getElementById("name-text");
                     var inputApellido = document.getElementById("last-name-text");
                     var inputCorreo = document.getElementById("email-text");
                     var inputContra = document.getElementById("password-text");
                     var mensajeError = document.getElementById("mensaje-error");
                     var mensajeError2 = document.getElementById("mensaje-error2");
                     var mensajeError3 = document.getElementById("mensaje-error3");
                     var mensajeError4 = document.getElementById("mensaje-error4");
             
                     // Agrega un controlador de eventos para el evento 'input' (cada vez que se escriba algo en el campo)
                     inputNombre.addEventListener("input", function() {
                         // Obtiene el valor del campo de entrada
                         var valor = inputNombre.value.trim();
             
                         // Realiza la validación, por ejemplo, si el campo no está vacío
                         if (valor === "") {
                             mensajeError.textContent = "El campo nombre es requerido.";
                         } else {
                             mensajeError.textContent = ""; // Limpia el mensaje de error si la validación pasa
                         }
                     });
                     // Agrega un controlador de eventos para el evento 'input' (cada vez que se escriba algo en el campo)
                     inputApellido.addEventListener("input", function() {
                         // Obtiene el valor del campo de entrada
                         var valor = inputApellido.value.trim();
             
                         // Realiza la validación, por ejemplo, si el campo no está vacío
                         if (valor === "") {
                             mensajeError2.textContent = "El campo nombre es requerido.";
                         } else {
                             mensajeError2.textContent = ""; // Limpia el mensaje de error si la validación pasa
                         }
                     });
                     // Agrega un controlador de eventos para el evento 'input' (cada vez que se escriba algo en el campo)
                     inputCorreo.addEventListener("input", function() {
                         // Obtiene el valor del campo de entrada
                         var valor = inputCorreo.value.trim();
             
                         // Realiza la validación, por ejemplo, si el campo no está vacío
                         if (valor === "") {
                             mensajeError3.textContent = "El campo nombre es requerido.";
                         } else {
                             mensajeError3.textContent = ""; // Limpia el mensaje de error si la validación pasa
                         }
                     });
                     // Agrega un controlador de eventos para el evento 'input' (cada vez que se escriba algo en el campo)
                     inputContra.addEventListener("input", function() {
                         // Obtiene el valor del campo de entrada
                         var valor = inputContra.value.trim();
             
                         // Realiza la validación, por ejemplo, si el campo no está vacío
                         if (valor === "") {
                             mensajeError4.textContent = "El campo nombre es requerido.";
                         } else {
                             mensajeError4.textContent = ""; // Limpia el mensaje de error si la validación pasa
                         }
                     });
    }, [navigate]);

    document.title = "Registro"

    return(
        <div className="login-screen-view">
            <div className="login-frame">
                <img src={userImage} alt="usuarioImagen" />
                <h1>Registro WikiSearch</h1>
                
                <input type="text" id="name-text" placeholder="Ingrese su nombre"/>
                <p id="mensaje-error" className="mensaje-error"></p>
                <input type="text" id="last-name-text" placeholder="Ingrese sus apellidos"/>
                <p id="mensaje-error2" className="mensaje-error"></p>
                <input type="text" id="email-text" placeholder="Ingrese su correo"/>
                <p id="mensaje-error3" className="mensaje-error"></p>
                <input type="password" id="password-text" placeholder="Ingrese su contraseña"/>
                <p id="mensaje-error4" className="mensaje-error"></p>

                

                <button className="submit-login" onClick={handleAccess}>
                    Confirmar
                </button>
                
            </div>
        </div>
        
    );
}