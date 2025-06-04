import torch
import torch.nn as nn

class TemperaturePredictorLSTM(nn.Module):
    def __init__(self, input_features, hidden_units, num_lstm_layers, output_size=1):
        super(TemperaturePredictorLSTM, self).__init__()
        self.hidden_units = hidden_units
        self.num_lstm_layers = num_lstm_layers

        self.lstm = nn.LSTM(input_features, hidden_units, num_lstm_layers, batch_first=True)

        self.linear = nn.Linear(hidden_units, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_lstm_layers, x.size(0), self.hidden_units).to(x.device)
        c0 = torch.zeros(self.num_lstm_layers, x.size(0), self.hidden_units).to(x.device)

        out, _ = self.lstm(x, (h0, c0))  # shape (batch_size, seq_length, hidden_units)

        out = self.linear(out[:, -1, :])
        return out