import express from 'express';
import connectDB from './config/db.js';
import Medicine from './models/medicineModel.js';

const app = express();
app.use(express.json());

connectDB();

app.get('/api/medicines', async (req, res) => {
  try {
    const medicines = await Medicine.find();
    res.json(medicines);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error fetching medicines.' });
  }
});

app.post('/api/medicines', async (req, res) => {
  const { name, expiryDate, quantity } = req.body;

  // Simple validation
  if (!name || !expiryDate || !quantity) {
    return res.status(400).json({ message: 'Name, expiry date, and quantity are required.' });
  }

  try {
    const newMedicine = new Medicine({
      name,
      expiryDate,
      quantity
    });

    await newMedicine.save();
    res.status(201).json(newMedicine);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Error saving the medicine.' });
  }
});

app.listen(5000, () => console.log('Server running on port 5000 🚀'));