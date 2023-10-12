
import React from 'react';
export default function ModalInfo(props) {
    return(
        <div className="modal-info" id="modal-info">
                <dialog open id="modalInfo">
                    <div className="border-modal-info">
                    </div>
                    <div className="logo-modal">
                        <span className="loader"></span>
                    </div>
                    <p>{props.text}</p>
                </dialog>
            </div>
    );
}