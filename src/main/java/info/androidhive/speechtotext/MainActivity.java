package info.androidhive.speechtotext;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.util.Log;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;


import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.Locale;
import java.net.URL;
import java.util.Map;
import java.util.*;

import javax.net.ssl.HttpsURLConnection;


public class MainActivity extends Activity {

	private TextView txtSpeechInput;
	private ImageButton btnSpeak;
	private Button Fire;
	private final int REQ_CODE_SPEECH_INPUT = 100;
    private String url;
    private RequestQueue queue;
    private String command;
    String respmsg = new String();
    private HashMap<String, String> MyData = new HashMap<String, String>();
    int responseCode2;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		txtSpeechInput = (TextView) findViewById(R.id.txtSpeechInput);
		btnSpeak = (ImageButton) findViewById(R.id.btnSpeak);
		Fire = (Button) findViewById(R.id.button3);
		getActionBar().hide();
		url = "http://192.168.1.202:80";
        //url="http://www.google.com";
		queue = Volley.newRequestQueue(this);

		btnSpeak.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				promptSpeechInput();
			}
		});
		Fire.setOnClickListener(new View.OnClickListener(){
			@Override
			public void onClick(View v){

                txtSpeechInput.setText("HTTP Button Pressed");
//				txtSpeechInput.setText("Rush B!")
//                StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
//                        new Response.Listener<String>() {
//                            @Override
//                            public void onResponse(String response) {
//								//txtSpeechInput.setText("Response is: "+ response.substring(0,500));
//
//                            }
//                        }, new Response.ErrorListener() {
//                    @Override
//                    public void onErrorResponse(VolleyError error) {
//                        //txtSpeechInput.setText(error.toString());
//                }
//                })
//				{
//                    protected Map<String, String> getParams() {
//                        MyData = new HashMap<String, String>();
//                        MyData.put("command", command);
//                        return MyData;
//                    }
//                };
//
//                queue.add(stringRequest);
//                new SendPostRequest().execute();
//                StringRequest stringRequest1 = new StringRequest(Request.Method.GET, url,
//                        new Response.Listener<String>() {
//                            @Override
//                            public void onResponse(String response) {
//                                // Display the first 500 characters of the response string.
//                                txtSpeechInput.setText("Response is: "+ response.substring(0,500));
//                            }
//                        }, new Response.ErrorListener() {
//                    @Override
//                    public void onErrorResponse(VolleyError error) {
//                        txtSpeechInput.setText(error.toString());
//                    }
//                });
//                queue.add(stringRequest1);

//                }

			}
		});

	}

	/**
	 * Showing google speech input dialog
	 * */
	private void promptSpeechInput() {
		Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
		intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
				RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
		intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
		intent.putExtra(RecognizerIntent.EXTRA_PROMPT,
				getString(R.string.speech_prompt));
		try {
			startActivityForResult(intent, REQ_CODE_SPEECH_INPUT);
		} catch (ActivityNotFoundException a) {
			Toast.makeText(getApplicationContext(),
					getString(R.string.speech_not_supported),
					Toast.LENGTH_SHORT).show();
		}
	}

	/**
	 * Receiving speech input
	 * */
	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		super.onActivityResult(requestCode, resultCode, data);

		switch (requestCode) {
		case REQ_CODE_SPEECH_INPUT: {
			if (resultCode == RESULT_OK && null != data) {

				ArrayList<String> result = data
						.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
				command = result.get(0);
                MyData.put("command", command);
				txtSpeechInput.setText(command);
			}
			break;
		}

		}
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}
	public class SendPostRequest extends AsyncTask<String, Void, String> {

		protected void onPreExecute(){}

		protected String doInBackground(String... arg0) {

			try{
				URL url = new URL("http://192.168.1.202");
				JSONObject postDataParams = new JSONObject();
                postDataParams.put(MyData.get("command"), "email");


				HttpURLConnection conn = (HttpURLConnection) url.openConnection();
				conn.setReadTimeout(3000 /* milliseconds */);
				conn.setConnectTimeout(3000 /* milliseconds */);
				conn.setRequestMethod("POST");
				conn.setDoInput(true);
				conn.setDoOutput(true);
				OutputStream os = conn.getOutputStream();
				BufferedWriter writer = new BufferedWriter(
						new OutputStreamWriter(os, "UTF-8"));
				writer.write(getPostDataString(postDataParams));
		        writer.flush();
				writer.close();
				os.close();

				respmsg = conn.getResponseMessage();
				int responseCode=conn.getResponseCode();
				responseCode2=responseCode;

			}
			catch(Exception e){
				return new String("Exception: " + e.getMessage());
			}
            return "";
		}

		@Override
		protected void onPostExecute(String result) {
			//txtSpeechInput.setText(respmsg);
		}


		public String getPostDataString(JSONObject params) throws Exception {

			StringBuilder result = new StringBuilder();
			boolean first = true;

			Iterator<String> itr = params.keys();

			while(itr.hasNext()){

				String key= itr.next();
				Object value = params.get(key);

				if (first)
					first = false;
				else
					result.append("&");

				result.append(URLEncoder.encode(key, "UTF-8"));
				result.append("=");
				result.append(URLEncoder.encode(value.toString(), "UTF-8"));

			}
			return result.toString();
		}

	}


}
