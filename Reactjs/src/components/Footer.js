import React from "react";
import "../styles/Footer.css";

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="row">
          <div className="col">
            <h5>COMPANY</h5>
            <ul>
              <li>
                <a href="#about">About Us</a>
              </li>
              <li>
                <a href="#contact">Contact Us</a>
              </li>
              <li>
                <a href="#services">Our Services</a>
              </li>
              <li>
                <a href="#privacy">Privacy Policy</a>
              </li>
              <li>
                <a href="#terms">Terms & Condition</a>
              </li>
            </ul>
          </div>
          <div className="col">
            <h5>QUICK LINKS</h5>
            <ul>
              <li>
                <a href="#about">Về chúng tôi</a>
              </li>
              <li>
                <a href="#contact">Contact Us</a>
              </li>
              <li>
                <a href="#services">Our Services</a>
              </li>
              <li>
                <a href="#privacy">Privacy Policy</a>
              </li>
              <li>
                <a href="#terms">Terms & Condition</a>
              </li>
            </ul>
          </div>
          <div className="col">
            <h5>CONTACT</h5>
            <p>123 Street, New York, USA</p>
            <p>+012 345 67890</p>
            <p>info@example.com</p>
            <div className="social-icons">
              <a href="#twitter">
                <i className="fab fa-twitter"></i>
              </a>
              <a href="#facebook">
                <i className="fab fa-facebook-f"></i>
              </a>
              <a href="#youtube">
                <i className="fab fa-youtube"></i>
              </a>
              <a href="#linkedin">
                <i className="fab fa-linkedin-in"></i>
              </a>
            </div>
          </div>
          <div className="col">
            <h5>NEWSLETTER</h5>
            <p>Subscribe to get the latest updates.</p>
            <div className="newsletter">
              <input type="email" placeholder="Your email" />
              <button>SignUp</button>
            </div>
          </div>
        </div>
        <div className="copyright">
          &copy; 2024 Your Site Name, All Rights Reserved. Designed by{" "}
          <a href="https://htmlcodex.com">HTML Codex</a>.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
