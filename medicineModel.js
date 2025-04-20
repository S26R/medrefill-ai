import mongoose from 'mongoose';

const medicineSchema = new mongoose.Schema({
  name: { type: String, required: true },
  expiryDate: { type: Date, required: true },
  quantity: { type: Number, required: true }
});

const Medicine = mongoose.model('Medicine', medicineSchema);

export default Medicine;