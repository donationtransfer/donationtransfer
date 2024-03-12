import express from "express";
import { json } from "body-parser";
import { hash, compare } from "bcrypt";
import { connect, query, close } from "mssql";
import { config } from "./config";

const app = express();

// Middleware
app.use(json());

// Register endpoint
app.post("/register", async (req, res) => {
	const { email, password } = req.body;

	try {
		// Hash password
		const hashedPassword = await hash(password, 10);
        
		await connect(config);
		const result = await query`INSERT INTO Users (Email, Password) VALUES (${email}, ${hashedPassword})`;
		res.json({ success: true });
	} catch (error) {
		console.error("Error during registration:", error);
		res.status(500).json({ success: false, message: "Registration failed" });
	} finally {
		close();
	}
});

// Login endpoint
app.post("/login", async (req, res) => {
	const { email, password } = req.body;

	try {
		await connect(config);
		const result = await query`SELECT * FROM Users WHERE Email = ${email}`;
		if (result.recordset.length === 1) {
			const user = result.recordset[0];
			const passwordMatch = await compare(password, user.Password);
			if (passwordMatch) {
				res.json({ success: true });
			} else {
				res.json({ success: false, message: "Invalid email or password" });
			}
		} else {
			res.json({ success: false, message: "Invalid email or password" });
		}
	} catch (error) {
		console.error("Error during login:", error);
		res.status(500).json({ success: false, message: "Login failed" });
	} finally {
		close();
	}
});

// Start server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
	console.log(`Server is running on port ${PORT}`);
});
