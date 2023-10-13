import React, { useState, useEffect } from "react";
import userImage from "../assets/user.png";
import Eye from "../assets/show-password-eye.png";
import NotEye from "../assets/hide-password-eye.png";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

export default function Register() {
  document.title = "Registro"
  const navigate = useNavigate();
  const handleAccess = () => {
    // Obtén una referencia al campo de entrada y al párrafo de mensaje de error
    var inputNombre = document.getElementById("name-text").value;
    var inputApellido = document.getElementById("last-name-text").value;
    var inputCorreo = document.getElementById("email-text").value;
    var inputContra = document.getElementById("password-text").value;
    var mensajeError = document.getElementById("mensaje-error");
    var mensajeError2 = document.getElementById("mensaje-error2");
    var mensajeError3 = document.getElementById("mensaje-error3");
    var mensajeError4 = document.getElementById("mensaje-error4");

    mensajeError.textContent = ""
    mensajeError2.textContent = ""
    mensajeError3.textContent = ""
    mensajeError4.textContent = ""

    // Agrega un controlador de eventos para el evento 'input' (cada vez que se escriba algo en el campo)
    const apiUrl = "http://172.17.0.2:5000/register";

    // Datos que deseas enviar en la solicitud POST
    if (inputNombre.trim() != ""
      && inputApellido.trim() != ""
      && inputCorreo.trim() != ""
      && inputContra.trim() != "") {
      const data = {
        name: inputNombre,
        lastName: inputApellido,
        email: inputCorreo,
        password: inputContra
      };

      // Realizar la solicitud POST
      axios
        .post(apiUrl, data)
        .then((response) => {
          console.log(response.data);
          if (response.data.status) {
            alert(response.data.message);
            navigate("/");
          } else {
            alert(response.data.message);
          }
        })
        .catch((error) => {
          // Si ocurre un error en la solicitud
          console.error("Error en la solicitud:", error);
        });
    } else {
      if (inputNombre.trim() === "") {
        mensajeError.textContent = "El campo 'Nombre' es necesario";

      }

      if (inputApellido.trim() === "") {
        mensajeError2.textContent = "El campo 'Apellido' es necesario";

      }
      if (inputContra.trim() === "") {
        mensajeError4.textContent = "El campo 'Contraseña' es necesario";

      }
      if (inputCorreo.trim() === "") {
        mensajeError3.textContent = "El campo 'Correo' es necesario";

      }
    }

  };
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
    inputNombre.addEventListener("input", function () {
      // Obtiene el valor del campo de entrada
      var valor = inputNombre.value.trim();

      // Realiza la validación, por ejemplo, si el campo no está vacío
      if (valor === "") {
        mensajeError.textContent = "El campo 'Nombre' es requerido.";
      } else {
        mensajeError.textContent = ""; // Limpia el mensaje de error si la validación pasa
      }
    });
    // Agrega un controlador de eventos para el evento 'input' (cada vez que se escriba algo en el campo)
    inputApellido.addEventListener("input", function () {
      // Obtiene el valor del campo de entrada
      var valor = inputApellido.value.trim();

      // Realiza la validación, por ejemplo, si el campo no está vacío
      if (valor === "") {
        mensajeError2.textContent = "El campo 'Apellido' es requerido.";
      } else {
        mensajeError2.textContent = ""; // Limpia el mensaje de error si la validación pasa
      }
    });
    // Agrega un controlador de eventos para el evento 'input' (cada vez que se escriba algo en el campo)
    inputCorreo.addEventListener("input", function () {
      // Obtiene el valor del campo de entrada
      var valor = inputCorreo.value.trim();

      // Realiza la validación, por ejemplo, si el campo no está vacío
      if (valor === "") {
        mensajeError3.textContent = "El campo 'Correo' es requerido.";
      } else {
        mensajeError3.textContent = ""; // Limpia el mensaje de error si la validación pasa
      }
    });
    // Agrega un controlador de eventos para el evento 'input' (cada vez que se escriba algo en el campo)
    inputContra.addEventListener("input", function () {
      // Obtiene el valor del campo de entrada
      var valor = inputContra.value.trim();

      // Realiza la validación, por ejemplo, si el campo no está vacío
      if (valor === "") {
        mensajeError4.textContent = "El campo 'Contraseña' es requerido.";
      } else {
        mensajeError4.textContent = ""; // Limpia el mensaje de error si la validación pasa
      }
    });
  }, [navigate]);



  return (
    <div className="login-screen-view">
      <div className="login-frame">
        <img src={userImage} alt="usuarioImagen" />
        <h1>Registro WikiSearch</h1>

        <input type="text" id="name-text" placeholder="Ingrese su nombre" />
        <p id="mensaje-error" className="mensaje-error"></p>
        <input
          type="text"
          id="last-name-text"
          placeholder="Ingrese sus apellidos"
        />
        <p id="mensaje-error2" className="mensaje-error"></p>
        <input type="text" id="email-text" placeholder="Ingrese su correo" />
        <p id="mensaje-error3" className="mensaje-error"></p>
        <input
          type="password"
          id="password-text"
          placeholder="Ingrese su contraseña"
        />
        <p id="mensaje-error4" className="mensaje-error"></p>

        <button className="submit-login" onClick={handleAccess}>
          Confirmar
        </button>
      </div>
    </div>
  );
}
