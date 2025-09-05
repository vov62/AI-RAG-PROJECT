import { Component, inject, signal, WritableSignal } from '@angular/core';
import { Skeleton } from "../../components/skeleton/skeleton";
import { HttpClient } from '@angular/common/http';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { ChatService } from '../../services/chat.service';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-home',
  imports: [Skeleton, ReactiveFormsModule, CommonModule],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home {

  private baseUrl: string = 'http://127.0.0.1:5000/api';
  private chatService = inject(ChatService)
  http = inject(HttpClient);

  userInput: WritableSignal<string> = signal('');
  aiResponse = signal<string>('');
  isLoading = signal(false);
  chatHistory = this.chatService.getHistory()

  formInput: FormGroup = new FormGroup({
    userInput: new FormControl(''),
  })


  sendQuery() {
    this.userInput.set(this.formInput.value.userInput)
    if (!this.userInput()?.trim()) return;
    this.isLoading.set(true)
    this.http.post(`${this.baseUrl}/query`, { query: this.userInput() }).subscribe({
      next: (res: any) => {
        // console.log('Query response:', res);
        this.chatService.addToHistory(this.userInput(), res.answer)
        // console.log(this.chatHistory);

        this.aiResponse.set(res.answer)
        this.formInput.reset();
        this.isLoading.set(false)
      },
      error: (err) => {
        console.error('Error from server:', err);
        this.isLoading.set(false);
      }
    })
  }



  testPing() {
    this.http.get(`${this.baseUrl}/ping`).subscribe({
      next: (res: any) => {
        console.log('Ping response:', res)
      }
    })
  }

}
