import { AfterViewInit, Component, ElementRef, inject, QueryList, signal, ViewChild, ViewChildren, WritableSignal } from '@angular/core';
import { Skeleton } from "../../components/skeleton/skeleton";
import { HttpClient } from '@angular/common/http';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ChatService } from '../../services/chat.service';
import { CommonModule } from '@angular/common';
import { marked } from 'marked';


@Component({
  selector: 'app-home',
  imports: [Skeleton, ReactiveFormsModule, CommonModule],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home implements AfterViewInit {

  private baseUrl: string = 'http://127.0.0.1:5000/api';
  private chatService = inject(ChatService)
  http = inject(HttpClient);

  @ViewChildren('message') messages!: QueryList<ElementRef>;

  userInput: WritableSignal<string> = signal('');
  // userInput = signal<string>('');
  aiResponse = signal<string>('');
  isLoading = signal(false);
  errorMessage = signal<string>('');
  chatHistory = this.chatService.getHistory()

  formInput: FormGroup = new FormGroup({
    userInput: new FormControl('', [Validators.required]),
  })

  ngAfterViewInit() {
    // ברגע שמספר ההודעות משתנה — גלול למטה
    this.messages.changes.subscribe(() => {
      this.scrollToBottom();
    });
  }


  sendQuery() {
    this.userInput.set(this.formInput.value.userInput)
    if (!this.userInput()?.trim()) return;
    this.isLoading.set(true)

    this.http.post(`${this.baseUrl}/query`, { query: this.userInput() }).subscribe({
      // this.chatService.postquery({ query: this.userInput }).subscribe({
      next: (res: any) => {
        // console.log('Query response:', res);
        this.chatService.addToHistory(this.userInput(), res.answer)
        // localStorage.setItem("user", this.chatHistory)
        // console.log(this.chatHistory);
        this.aiResponse.set(res.answer)
        this.formInput.reset();
        this.isLoading.set(false)
      },
      error: (err) => {
        console.error('Error from server:', err);
        this.errorMessage.set('something went wrong, try to refresh the page')
        this.isLoading.set(false);
      }
    })
  }

  private scrollToBottom() {
    const container = document.querySelector('.chat-history');
    if (container) {
      container.scrollTo({
        top: container.scrollHeight,
        behavior: 'smooth'

      })
    }
  }


  formatAIResponse(response: string): string {
    if (!response) return '';

    // מחליף כוכביות בטקסט מודגש
    const cleanText = response.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // מפרק שורות שמתחילות ב* לרשימה
    const html = cleanText
      .split('\n')
      .map(line => line.trim().startsWith('*')
        ? `<li>${line.replace('*', '').trim()}</li>`
        : `<p>${line}</p>`)
      .join('');

    return `<ul dir="rtl">${html}</ul>`;
  }

}
