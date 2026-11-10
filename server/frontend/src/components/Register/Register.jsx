
import React, { useState } from "react";
import "./Register.css";

export default function Register() {
  const [form, setForm] = useState({
    userName: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage("");

    if (Object.values(form).some((value) => !value.trim())) {
      setMessage("Please complete all required fields.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("/djangoapp/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify(form),
      });

      const result = await response.json();

      if (!response.ok) {
        setMessage(result.message || result.error ||
          "Registration failed.");
        return;
      }

      setMessage("Registration successful! You can now log in.");

      setForm({
        userName: "",
        firstName: "",
        lastName: "",
        email: "",
        password: "",
      });
    } catch (error) {
      setMessage("Unable to connect to the registration server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container py-5">
      <div className="card shadow-sm mx-auto"
           style={{ maxWidth: "520px" }}>
        <div className="card-body p-4">
          <h2 className="text-center mb-3">Sign Up</h2>
          <p className="text-center text-muted">
            Create your Cars Dealership account
          </p>

          <form onSubmit={handleSubmit}>
            {[
              ["userName", "Username", "text"],
              ["firstName", "First Name", "text"],
              ["lastName", "Last Name", "text"],
              ["email", "Email", "email"],
              ["password", "Password", "password"],
            ].map(([name, label, type]) => (
              <div className="mb-3" key={name}>
                <label htmlFor={name} className="form-label">
                  {label}
                </label>
                <input
                  id={name}
                  name={name}
                  type={type}
                  className="form-control"
                  value={form[name]}
                  onChange={handleChange}
                  autoComplete={
                    name === "password" ? "new-password" : "on"
                  }
                  required
                />
              </div>
            ))}

            {message && (
              <div role="status" className="alert alert-info">
                {message}
              </div>
            )}

            <button
              type="submit"
              className="btn btn-primary w-100"
              disabled={loading}
            >
              {loading ? "Registering..." : "Register"}
            </button>
          </form>

          <p className="text-center mt-3">
            Already have an account?{" "}
            <a href="/login">Login</a>
          </p>
        </div>
      </div>
    </main>
  );
}
