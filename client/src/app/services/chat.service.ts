import { HttpClient, HttpHeaders } from '@angular/common/http';
import { inject, Injectable, signal } from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class ChatService {

    http = inject(HttpClient)
    chatHistory = signal<{ user: string, bot: string }[]>([]);
    private baseUrl: string = 'http://127.0.0.1:5000/api';

    // שליחת יוזר אינפוט
    postquery(userQuery: { query: string }) {
        return this.http.post(`${this.baseUrl}/query`, userQuery)
    }
    // ניסוח טקסט מחדש
    rephraseQuery(query: string) {
        const headers = new HttpHeaders({ 'Content-Type': 'application/json' })
        return this.http.post(`${this.baseUrl}/rephrase`, { query }, { headers });
    }

    // הוספת טקסט להיסטוריה
    addToHistory(userInput: string, aiResponse: string) {
        this.chatHistory.update(history => [
            ...history,
            { user: userInput, bot: aiResponse }
        ]);
        this.saveHistoryToLocalStorage();
        return this.chatHistory
    }

    getHistory() {
        return this.chatHistory;
    }

    private saveHistoryToLocalStorage() {
        localStorage.setItem("chatHistory", JSON.stringify(this.chatHistory()));
    }
    loadHistoryFromLocalStorage() {
        const savedHistory = localStorage.getItem("chatHistory");
        if (savedHistory) {
            this.chatHistory.set(JSON.parse(savedHistory));
        }
    }




}
