using System;
using System.Drawing;
using System.Windows.Forms;
using mcp2221_JA;
using System.Globalization;

namespace UpdateUSBRTC
{
    public partial class UpdateUSBRTC : Form
    {
        IntPtr HandleMCP2221;
        myDLL myDLLmcp2221 = new myDLL();
        bool flagAMPM = false;

        public UpdateUSBRTC()
        {
            InitializeComponent();
            myDLLmcp2221.Init();
            // Check format Time and Date to display
            if (CultureInfo.CurrentCulture.Name == "en-US")
            {
                flagAMPM = true;
                radiobuttonMMDDYY.Checked = true;
            }
            else
            {
                flagAMPM = false;
                radiobuttonDDMMYY.Checked = true;
            }
            // Check if a mcp2221 is connected to the computer 
            if (myDLLmcp2221.checkMCP2221Present())
            {
                try
                {
                    if (myDLLmcp2221.getHandle(out HandleMCP2221, out string stReturn))
                    {
                        labelResultat.ForeColor = Color.Green;
                        buttonAction.Text = "Update";
                    }
                    else
                    {
                        labelResultat.ForeColor = Color.Red;
                        buttonAction.Text = "Search";
                    }
                    labelResultat.Text = stReturn;
                }
                catch (Exception)
                {
                    labelResultat.ForeColor = Color.Red;
                    buttonAction.Text = "Exit";
                    labelResultat.Text = "Load DLL ERROR";
                }

            }
        }

        private void btUpdate_Click(object sender, EventArgs e)
        {
            switch (buttonAction.Text)
            {
                case "Connect":
                    // Check if a mcp2221 is connected to the computer 
                    if (myDLLmcp2221.checkMCP2221Present())
                    {
                        if (myDLLmcp2221.getHandle(out HandleMCP2221, out string stConnect))
                        {
                            labelResultat.ForeColor = Color.Green;
                            buttonAction.Text = "Update";
                        }
                        else
                        {
                            labelResultat.ForeColor = Color.Red;
                            buttonAction.Text = "Search";
                        }
                        labelResultat.Text = stConnect;
                    }
                    break;
                case "Search":
                    if (myDLLmcp2221.getHandle(out HandleMCP2221, out string stReturn))
                    {
                        labelResultat.ForeColor = Color.Green;
                        buttonAction.Text = "Update";
                    }
                    else
                    {
                        labelResultat.ForeColor = Color.Red;
                    }
                    labelResultat.Text = stReturn;
                    break;
                case "Update":
                    if (myDLLmcp2221.updateMCP2221(HandleMCP2221, radiobuttonMMDDYY.Checked))
                    {
                        buttonAction.Text = "Check";
                        radiobuttonDDMMYY.Enabled = false;
                        radiobuttonMMDDYY.Enabled = false;
                    }
                    break;
                case "Check":
                    string stResult = "";
                    if (myDLLmcp2221.checkMCP2221(HandleMCP2221, out stResult, out flagAMPM))
                    {
                        buttonAction.Text = "Exit";
                        labelResultat.ForeColor = Color.Green;
                    }
                    else
                    {
                        labelResultat.ForeColor = Color.Red;
                    }
                    labelResultat.Text = stResult;
                    break;
                case "Exit":
                    Application.Exit();
                    break;
                default:
                    break;
            }
        }
    }
}

