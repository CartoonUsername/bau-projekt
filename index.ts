// Beispiel: Video mit Seedance 2.5 (Text-to-Video) über die Higgsfield API erzeugen.
// Start: npm run video   (lädt HF_CREDENTIALS aus .env.local, Format key-id:key-secret)
import {
  createHiggsfieldClient,
  AuthenticationError,
  NotEnoughCreditsError,
  TimeoutError,
  APIError,
} from "@higgsfield/client/v2";

const MODEL = "bytedance/seedance-2.5/text-to-video";

// Zugangsdaten nur serverseitig aus der Umgebung lesen, nie ausgeben oder loggen.
const credentials = process.env.HF_CREDENTIALS?.trim();
if (!credentials || !/^[^:\s]+:[^:\s]+$/.test(credentials)) {
  console.error("HF_CREDENTIALS fehlt oder hat nicht das Format key-id:key-secret. Bitte lokal in .env.local eintragen.");
  process.exit(1);
}

const client = createHiggsfieldClient({
  credentials,
  maxPollTime: 15 * 60 * 1000, // Videos können länger als der Standard von 5 Minuten brauchen
});

async function main(): Promise<void> {
  const result = await client.subscribe(MODEL, {
    input: {
      prompt: "A cinematic scene at sunset",
      duration: 5,
      resolution: "720p",
      aspect_ratio: "16:9",
    },
    withPolling: true, // wartet, bis die Anfrage fertig, fehlgeschlagen oder moderiert ist
  });

  // Die SDK-Typen kennen "canceled" nicht, die API kann es aber melden.
  const status = String(result.status);
  switch (status) {
    case "completed": {
      const url = result.video?.url;
      if (!url) {
        console.error(`Anfrage ${result.request_id} ist abgeschlossen, enthält aber keine Video-URL.`);
        process.exit(1);
      }
      console.log(`Video-URL: ${url}`);
      return;
    }
    case "nsfw":
      console.error(`Anfrage ${result.request_id} wurde von der Moderation abgelehnt (Credits werden erstattet).`);
      process.exit(2);
    case "failed":
      console.error(`Anfrage ${result.request_id} ist fehlgeschlagen (Credits werden erstattet).`);
      process.exit(3);
    case "canceled":
    case "cancelled":
      console.error(`Anfrage ${result.request_id} wurde abgebrochen.`);
      process.exit(4);
    default:
      console.error(`Anfrage ${result.request_id} ist nicht abgeschlossen (Status: ${status}).`);
      process.exit(5);
  }
}

main().catch((error: unknown) => {
  if (error instanceof AuthenticationError) {
    console.error("Anmeldung abgelehnt: HF_CREDENTIALS prüfen (key-id:key-secret).");
  } else if (error instanceof NotEnoughCreditsError) {
    console.error("Nicht genug Credits oder Zugriff verweigert (HTTP 403).");
  } else if (error instanceof TimeoutError) {
    console.error(`Zeitüberschreitung beim Warten auf das Video: ${error.message}`);
  } else if (error instanceof APIError) {
    console.error(`API-Fehler (HTTP ${error.statusCode ?? "?"}): ${error.message}`);
  } else {
    console.error(`Unerwarteter Fehler: ${error instanceof Error ? error.message : String(error)}`);
  }
  process.exit(1);
});
