import React, { useState } from 'react';
import './Navbar.css';
import { Link } from 'react-router-dom';

const Navbar = () => {
    const [menu, setMenu] = useState("shop");

    return (
        <div className='navbar'>
            <div className='nav-logo'>
                {/* <img src={logo} alt='logo' /> */}
                <p>THULIRISE</p>
            </div>

            <ul className='nav-menu'>
                <li onClick={() => { setMenu("shop") }}>
                    <Link className={`li-tag ${menu === "shop" ? "active" : ""}`} to='/'>Shop</Link>
                </li>
                <li onClick={() => { setMenu("upload") }}>
                    <Link className={`li-tag ${menu === "upload" ? "active" : ""}`} to='/upload'>Upload</Link>
                </li>
                <li onClick={() => { setMenu("signup") }}>
                    <Link className={`li-tag ${menu === "signup" ? "active" : ""}`} to='/signup'>Sign Up</Link>
                </li>
            </ul>
        </div>
    );
};

export default Navbar;
